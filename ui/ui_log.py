
from __future__ import annotations

from typing import Dict

from PySide6.QtCore import QDateTime, QObject, QRect, QSize, Qt, Signal, QModelIndex
from PySide6.QtGui import QColor, QFont, QFontMetrics, QIntValidator, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStyledItemDelegate,
    QStyle,
    QStyleOptionViewItem,
    QVBoxLayout,
    QWidget,
)

from ore_data import Ore, OreDatabase, Tier
from .ui_theme import UiTheme, norm_variant, tier_color, variant_color, VARIANTS


class LogFindDialog(QDialog):
    def __init__(self, ore_db: OreDatabase, theme: UiTheme, initial_variant: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.ore_db = ore_db
        self.theme = theme
        self.setWindowTitle("Log Find")
        self.setModal(True)
        self.resize(720, 560)
        self._variant = norm_variant(initial_variant)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        title = QLabel("Log a Find")
        title.setStyleSheet("font-size: 18pt; font-weight: 950;")
        layout.addWidget(title)

        results_box = QFrame()
        results_box.setObjectName("DialogListBox")
        results_layout = QVBoxLayout(results_box)
        results_layout.setContentsMargins(14, 14, 14, 14)
        results_layout.setSpacing(10)

        hint = QLabel("Pick an ore from the list below.")
        hint.setStyleSheet("color: rgba(169,177,195,0.9); font-weight: 650;")
        results_layout.addWidget(hint)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search ore…")
        results_layout.addWidget(self.search)

        self.results = QListWidget()
        self.results.setStyleSheet("QListWidget{background:transparent;}")
        results_layout.addWidget(self.results, 1)

        layout.addWidget(results_box, 3)

        details = QFrame()
        details.setObjectName("DialogDetails")
        details_layout = QVBoxLayout(details)
        details_layout.setContentsMargins(14, 12, 14, 12)
        details_layout.setSpacing(10)

        details_title = QLabel("Details")
        details_title.setObjectName("DialogSectionTitle")
        details_layout.addWidget(details_title)

        vrow = QHBoxLayout()
        vrow.setContentsMargins(0, 0, 0, 0)
        vrow.setSpacing(10)
        vlabel = QLabel("Variant")
        vlabel.setFixedWidth(120)
        vrow.addWidget(vlabel)
        self.variant_combo = QComboBox()
        for key, label, _c in VARIANTS:
            self.variant_combo.addItem(label, userData=key)
        idx = self.variant_combo.findData(self._variant)
        if idx >= 0:
            self.variant_combo.setCurrentIndex(idx)
        vrow.addWidget(self.variant_combo, 1)
        details_layout.addLayout(vrow)

        d_row = QHBoxLayout()
        d_row.setContentsMargins(0, 0, 0, 0)
        d_row.setSpacing(10)
        dlabel = QLabel("Date")
        dlabel.setFixedWidth(120)
        d_row.addWidget(dlabel)
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDateTime.currentDateTime().date())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        d_row.addWidget(self.date_edit, 1)
        details_layout.addLayout(d_row)

        m_row = QHBoxLayout()
        m_row.setContentsMargins(0, 0, 0, 0)
        m_row.setSpacing(10)
        mlabel = QLabel("Mined")
        mlabel.setFixedWidth(120)
        m_row.addWidget(mlabel)
        self.mined_edit = QLineEdit()
        self.mined_edit.setPlaceholderText("Required (e.g. 250)")
        self.mined_edit.setValidator(QIntValidator(1, 2_147_483_647, self))
        m_row.addWidget(self.mined_edit, 1)
        details_layout.addLayout(m_row)

        layout.addWidget(details, 2)

        btn_row = QHBoxLayout()
        btn_row.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn = QPushButton("Log")
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.ok_btn)
        layout.addLayout(btn_row)

        self.cancel_btn.clicked.connect(self.reject)
        self.ok_btn.clicked.connect(self._try_accept)

        self.search.textChanged.connect(self._refresh_results)
        self.results.itemDoubleClicked.connect(lambda _it: self._try_accept())
        self.variant_combo.currentIndexChanged.connect(lambda _i: self._on_variant_changed())
        self.results.currentItemChanged.connect(lambda _cur, _prev: self._on_selected_changed())

        self._all = self.ore_db.get_all_ores()
        self._ore_by_key = {o.key: o for o in self._all}
        self._results_delegate = LogFindResultsDelegate(theme=self.theme, variant=self.selected_variant(), ore_by_key=self._ore_by_key, parent=self.results)
        self.results.setItemDelegate(self._results_delegate)
        self.results.setSpacing(4)
        self.results.setStyleSheet(
            "QListWidget{background:transparent;}"
            "QListWidget::item{background:transparent;border:none;margin:0;padding:0;}"
        )
        self._refresh_results()
        self._on_selected_changed()

    def _on_variant_changed(self):
        try:
            self._on_selected_changed()
            self._results_delegate.set_variant(self.selected_variant())
            self.results.viewport().update()
        except Exception:
            pass

    def _set_normal_enabled(self, enabled: bool) -> None:
        try:
            m = self.variant_combo.model()
            idx = self.variant_combo.findData("normal")
            if idx >= 0 and hasattr(m, "item"):
                it = m.item(idx)
                if it is not None:
                    it.setEnabled(bool(enabled))
        except Exception:
            pass

    def _on_selected_changed(self):
        k = self.selected_ore_key()
        if not k:
            self._set_normal_enabled(True)
            return
        ore = self._ore_by_key.get(str(k))
        if ore is None:
            self._set_normal_enabled(True)
            return
        if ore.tier == Tier.EXOTIC:
            self._set_normal_enabled(False)
            if self.selected_variant() == "normal":
                idx = self.variant_combo.findData("ionized")
                if idx >= 0:
                    self.variant_combo.setCurrentIndex(idx)
        else:
            self._set_normal_enabled(True)

    def _try_accept(self):
        ore_key = self.selected_ore_key()
        if not ore_key:
            QMessageBox.information(self, "Select an Ore", "Please select an ore to log.")
            return
        ore = self._ore_by_key.get(str(ore_key))
        if ore is not None and ore.tier == Tier.EXOTIC and self.selected_variant() == "normal":
            QMessageBox.information(self, "Cannot Log Exotic", "Exotic ores must be logged as Ionized or Spectral.")
            return
        mined = self.selected_mined()
        if mined is None or mined < 1:
            QMessageBox.information(self, "Mined Required", "Please enter how many mined (at least 1).")
            try:
                self.mined_edit.setFocus()
            except Exception:
                pass
            return
        self.accept()

    def _refresh_results(self):
        q = (self.search.text() or "").strip().lower()
        self.results.clear()
        ores = self._all
        if q:
            ores = [o for o in ores if q in o.name.lower()]
        ores = ores[:200]
        for o in ores:
            item = QListWidgetItem("")
            item.setData(Qt.ItemDataRole.UserRole, o.key)
            self.results.addItem(item)
        if self.results.count() > 0:
            self.results.setCurrentRow(0)

    def selected_ore_key(self) -> str | None:
        item = self.results.currentItem()
        if not item:
            return None
        k = item.data(Qt.ItemDataRole.UserRole)
        return str(k) if k else None

    def selected_date_iso(self) -> str:
        return self.date_edit.date().toString("yyyy-MM-dd")

    def selected_mined(self) -> int | None:
        s = (self.mined_edit.text() or "").strip()
        if not s:
            return None
        try:
            v = int(s)
            return v if v >= 1 else None
        except Exception:
            return None

    def selected_variant(self) -> str:
        v = self.variant_combo.currentData()
        return norm_variant(str(v) if v else "normal")


class LogEntryDelegate(QStyledItemDelegate):
    def __init__(self, theme: UiTheme, parent: QObject | None = None):
        super().__init__(parent)
        self.theme = theme
        self.font_name = QFont("Segoe UI", 11, QFont.Weight.DemiBold)
        self.font_meta = QFont("Segoe UI", 9, QFont.Weight.DemiBold)
        self._fm_name = QFontMetrics(self.font_name)
        self._fm_meta = QFontMetrics(self.font_meta)

    @staticmethod
    def _delete_rect(card_rect: QRect, pad_x: int) -> QRect:
        d = 20
        return QRect(card_rect.right() - pad_x - d, card_rect.center().y() - d // 2, d, d)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.save()
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

            data = index.data(Qt.ItemDataRole.UserRole)
            if not isinstance(data, dict):
                return super().paint(painter, option, index)

            ore_name = str(data.get("ore_name") or "")
            variant = norm_variant(str(data.get("variant") or "normal"))
            tier_name = str(data.get("tier") or "")
            world_name = str(data.get("world") or "")
            mined = data.get("mined")

            date_raw = str(data.get("date") or "")
            dt_raw = str(data.get("dt") or "")
            qd = None
            if date_raw:
                d = QDateTime.fromString(date_raw, "yyyy-MM-dd")
                qd = d.date() if d.isValid() else None
            if qd is None and dt_raw:
                d2 = QDateTime.fromString(dt_raw, "yyyy-MM-dd HH:mm")
                qd = d2.date() if d2.isValid() else None
            if qd is None:
                qd = QDateTime.currentDateTime().date()

            date_full = qd.toString("dd/MM/yyyy")
            date_short = qd.toString("dd/MM/yy")
            date_tiny = qd.toString("dd/MM")

            base = option.rect.adjusted(6, 6, -6, -6)
            w = base.width()
            pad_x = 12 if w >= 520 else (10 if w >= 420 else (8 if w >= 320 else 6))
            gap = 10 if w >= 520 else (8 if w >= 420 else (6 if w >= 320 else 4))
            r = base
            is_selected = bool(option.state & QStyle.StateFlag.State_Selected)
            bg = self.theme.card_hover if is_selected else self.theme.card

            path = QPainterPath()
            path.addRoundedRect(r, 12, 12)
            painter.fillPath(path, bg)
            painter.setPen(QPen(self.theme.border, 1))
            painter.drawPath(path)

            y_mid = r.top() + r.height() // 2

            v_label_full = next((lbl for k, lbl, _c in VARIANTS if k == variant), variant.title())
            v_label_short = {"normal": "N", "ionized": "I", "spectral": "S"}.get(variant, v_label_full[:1])
            v_col = variant_color(variant)
            painter.setFont(self.font_meta)
            v_text_w_full = self._fm_meta.horizontalAdvance(v_label_full)
            v_text_w_short = self._fm_meta.horizontalAdvance(v_label_short)
            v_h = 22
            v_w_full = max(78, min(140, v_text_w_full + 22))
            v_w_short = max(46, min(80, v_text_w_short + 20))

            t_label_full = tier_name if tier_name else "Tier"
            t_label_short = (tier_name[:3].upper() if tier_name else "T")
            t_text_w_full = self._fm_meta.horizontalAdvance(t_label_full)
            t_text_w_short = self._fm_meta.horizontalAdvance(t_label_short)
            t_h = 22
            t_w_full = max(78, min(170, t_text_w_full + 22))
            t_w_short = max(54, min(90, t_text_w_short + 20))

            date_h = 22
            date_w_full = max(92, min(140, self._fm_meta.horizontalAdvance(date_full) + 22))
            date_w_short = max(76, min(120, self._fm_meta.horizontalAdvance(date_short) + 22))
            date_w_tiny = max(64, min(96, self._fm_meta.horizontalAdvance(date_tiny) + 20))

            min_name_w = 60
            del_rect = self._delete_rect(r, pad_x)
            full_need = (pad_x * 3 + gap * 4 + date_w_full + t_w_full + v_w_full + min_name_w + del_rect.width())
            use_short_variant = (w < full_need)
            short_variant_need = (pad_x * 3 + gap * 4 + date_w_full + t_w_full + v_w_short + min_name_w + del_rect.width())
            use_short_tier = (w < short_variant_need)
            v_label = v_label_short if use_short_variant else v_label_full
            v_w = v_w_short if use_short_variant else v_w_full
            v_rect = QRect(del_rect.left() - gap - v_w, y_mid - v_h // 2, v_w, v_h)
            t_label = t_label_short if use_short_tier else t_label_full
            t_w = t_w_short if use_short_tier else t_w_full
            t_rect = QRect(v_rect.left() - gap - t_w, y_mid - t_h // 2, t_w, t_h)

            mined_text_full = ""
            mined_text_short = ""
            mined_w_full = 0
            mined_w_short = 0
            mined_h = 22
            try:
                mined_val = int(mined) if mined is not None and str(mined).strip() != "" else None
            except Exception:
                mined_val = None
            if mined_val is not None:
                mined_text_full = f"{mined_val:,} Mined"
                mined_text_short = f"x{mined_val:,}"
                mined_w_full = max(92, min(160, self._fm_meta.horizontalAdvance(mined_text_full) + 22))
                mined_w_short = max(56, min(110, self._fm_meta.horizontalAdvance(mined_text_short) + 20))

            remaining_for_date = t_rect.left() - (r.left() + pad_x) - gap - min_name_w
            if mined_val is not None:
                remaining_for_date -= (gap + mined_w_full)
            if remaining_for_date >= date_w_full:
                date_text = date_full
                date_w = date_w_full
            elif remaining_for_date >= date_w_short:
                date_text = date_short
                date_w = date_w_short
            else:
                date_text = date_tiny
                date_w = min(date_w_tiny, max(52, remaining_for_date))

            date_rect = QRect(r.left() + pad_x, y_mid - date_h // 2, date_w, date_h)

            mined_rect = QRect(0, 0, 0, 0)
            use_short_mined = False
            if mined_val is not None:
                remaining_for_mined = t_rect.left() - (date_rect.right() + gap) - gap - min_name_w
                use_short_mined = remaining_for_mined < mined_w_full
                mw = mined_w_short if use_short_mined else mined_w_full
                mined_rect = QRect(date_rect.right() + gap, y_mid - mined_h // 2, mw, mined_h)

            name_left = (mined_rect.right() + gap) if mined_val is not None else (date_rect.right() + gap)
            name_right = t_rect.left() - gap

            date_bg = QColor(self.theme.panel)
            date_bg.setAlpha(140)
            date_border = QColor(self.theme.border)
            date_border.setAlpha(180)
            d_path = QPainterPath()
            d_path.addRoundedRect(date_rect, date_h / 2, date_h / 2)
            painter.fillPath(d_path, date_bg)
            painter.setPen(QPen(date_border, 1))
            painter.drawPath(d_path)
            painter.setPen(self.theme.fg_muted)
            painter.drawText(date_rect, Qt.AlignmentFlag.AlignCenter, date_text)

            if mined_val is not None:
                m_bg = QColor(self.theme.panel)
                m_bg.setAlpha(140)
                m_border = QColor(self.theme.border)
                m_border.setAlpha(180)
                m_path = QPainterPath()
                m_path.addRoundedRect(mined_rect, mined_h / 2, mined_h / 2)
                painter.fillPath(m_path, m_bg)
                painter.setPen(QPen(m_border, 1))
                painter.drawPath(m_path)
                painter.setPen(self.theme.fg_muted)
                painter.drawText(mined_rect, Qt.AlignmentFlag.AlignCenter, mined_text_short if use_short_mined else mined_text_full)

            if tier_name:
                if world_name == "Natura" and tier_name == "Zenith":
                    t_bg = QColor("#000000")
                    t_border = QColor("#000000")
                    t_border.setAlpha(200)
                    t_fg = QColor("#ffffff")
                else:
                    basec = tier_color(self.theme, tier_name)
                    t_bg = QColor(basec)
                    t_bg.setAlpha(70)
                    t_border = QColor(basec)
                    t_border.setAlpha(170)
                    t_fg = QColor(basec).darker(190) if basec.lightness() > 150 else QColor(basec).lighter(185)
                t_path = QPainterPath()
                t_path.addRoundedRect(t_rect, t_h / 2, t_h / 2)
                painter.fillPath(t_path, t_bg)
                painter.setPen(QPen(t_border, 1))
                painter.drawPath(t_path)
                painter.setPen(t_fg)
                painter.drawText(t_rect, Qt.AlignmentFlag.AlignCenter, t_label)

            v_bg = QColor(v_col)
            v_bg.setAlpha(60)
            v_border = QColor(v_col)
            v_border.setAlpha(150)
            v_path = QPainterPath()
            v_path.addRoundedRect(v_rect, v_h / 2, v_h / 2)
            painter.fillPath(v_path, v_bg)
            painter.setPen(QPen(v_border, 1))
            painter.drawPath(v_path)
            painter.setPen(QColor(v_col).lighter(115))
            painter.drawText(v_rect, Qt.AlignmentFlag.AlignCenter, v_label)

            hovered_del = False
            try:
                hovered_del = bool(option.widget and hasattr(option.widget, "is_delete_hovered") and option.widget.is_delete_hovered(int(index.data(Qt.ItemDataRole.UserRole + 1) or -1)))
            except Exception:
                hovered_del = False

            if hovered_del:
                del_bg = QColor("#FF4D4D")
                del_bg.setAlpha(110)
                del_border = QColor("#FF4D4D")
                del_border.setAlpha(220)
                x_pen = QColor("#FF4D4D")
                x_pen.setAlpha(255)
            else:
                del_bg = QColor(self.theme.panel)
                del_bg.setAlpha(160)
                del_border = QColor(self.theme.border)
                del_border.setAlpha(200)
                x_pen = QColor(self.theme.fg_muted)
                x_pen.setAlpha(220)
            del_path = QPainterPath()
            del_path.addEllipse(del_rect)
            painter.fillPath(del_path, del_bg)
            painter.setPen(QPen(del_border, 1))
            painter.drawPath(del_path)
            painter.setPen(QPen(x_pen, 2))
            pad = 6
            painter.drawLine(del_rect.left() + pad, del_rect.top() + pad, del_rect.right() - pad, del_rect.bottom() - pad)
            painter.drawLine(del_rect.left() + pad, del_rect.bottom() - pad, del_rect.right() - pad, del_rect.top() + pad)

            painter.setFont(self.font_name)
            glow = variant_color(variant)
            base = QColor(self.theme.fg)
            name_color = QColor(
                int(base.red() * 0.65 + glow.red() * 0.35),
                int(base.green() * 0.65 + glow.green() * 0.35),
                int(base.blue() * 0.65 + glow.blue() * 0.35),
            )
            name_rect = QRect(name_left, y_mid - 12, max(0, name_right - name_left), 24)
            elided = self._fm_name.elidedText(ore_name, Qt.TextElideMode.ElideRight, name_rect.width())

            glow1 = QColor(glow)
            glow1.setAlpha(82)
            painter.setPen(glow1)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                painter.drawText(name_rect.translated(dx, dy), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, elided)
            glow2 = QColor(glow)
            glow2.setAlpha(46)
            painter.setPen(glow2)
            for dx, dy in [(-2, 0), (2, 0)]:
                painter.drawText(name_rect.translated(dx, dy), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, elided)

            painter.setPen(name_color)
            painter.drawText(name_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, elided)
        finally:
            painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(0, 52)


class LogFindResultsDelegate(QStyledItemDelegate):
    def __init__(self, theme: UiTheme, variant: str, ore_by_key: Dict[str, Ore], parent: QObject | None = None):
        super().__init__(parent)
        self.theme = theme
        self.variant = norm_variant(variant)
        self.ore_by_key = ore_by_key

        self.font_name = QFont("Segoe UI", 12, QFont.Weight.DemiBold)
        self.font_pill = QFont("Segoe UI", 10, QFont.Weight.Bold)
        self._name_metrics = QFontMetrics(self.font_name)
        self._pill_metrics = QFontMetrics(self.font_pill)

    def set_variant(self, variant: str):
        self.variant = norm_variant(variant)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(0, 46)

    @staticmethod
    def _rounded_rect_path(rect: QRect, radius: float) -> QPainterPath:
        p = QPainterPath()
        p.addRoundedRect(rect, radius, radius)
        return p

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.save()
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            ore_key = index.data(Qt.ItemDataRole.UserRole)
            ore = self.ore_by_key.get(str(ore_key), None)
            if ore is None:
                return

            is_hover = bool(option.state & QStyle.StateFlag.State_MouseOver)
            is_selected = bool(option.state & QStyle.StateFlag.State_Selected)

            r = option.rect.adjusted(8, 4, -8, -4)
            bg = self.theme.card_hover if (is_hover or is_selected) else self.theme.card
            path = self._rounded_rect_path(r, 14)
            painter.fillPath(path, bg)
            painter.setPen(QPen(self.theme.border, 1))
            painter.drawPath(path)

            painter.setFont(self.font_name)
            glow = variant_color(self.variant)
            base = QColor(self.theme.fg)
            name_color = QColor(
                int(base.red() * 0.65 + glow.red() * 0.35),
                int(base.green() * 0.65 + glow.green() * 0.35),
                int(base.blue() * 0.65 + glow.blue() * 0.35),
            )
            name_rect = QRect(r.left() + 14, r.top(), r.width() - 220, r.height())
            elided = self._name_metrics.elidedText(ore.name, Qt.TextElideMode.ElideRight, name_rect.width())

            glow1 = QColor(glow)
            glow1.setAlpha(72)
            painter.setPen(glow1)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                painter.drawText(name_rect.translated(dx, dy), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, elided)
            painter.setPen(name_color)
            painter.drawText(name_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, elided)

            tier_name = ore.tier.value
            right_x = r.right() - 12
            pill_h = 24
            painter.setFont(self.font_pill)
            pad_x = 12
            w = max(78, min(220, self._pill_metrics.horizontalAdvance(tier_name) + pad_x * 2))
            rect = QRect(right_x - w, r.center().y() - pill_h // 2, w, pill_h)
            pill_path = self._rounded_rect_path(rect, pill_h / 2)
            if ore.world == "Natura" and tier_name == "Zenith":
                fill = QColor("#000000")
                border = QColor("#000000")
                border.setAlpha(200)
                fg = QColor("#ffffff")
            else:
                basec = tier_color(self.theme, tier_name)
                fill = QColor(basec)
                fill.setAlpha(70)
                border = QColor(basec)
                border.setAlpha(170)
                fg = QColor(basec).darker(190) if basec.lightness() > 150 else QColor(basec).lighter(185)
            painter.fillPath(pill_path, fill)
            painter.setPen(QPen(border, 1))
            painter.drawPath(pill_path)
            painter.setPen(fg)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, tier_name)
        finally:
            painter.restore()


class LogListWidget(QListWidget):
    deleteRequested = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self._hover_delete_idx: int | None = None

    def is_delete_hovered(self, log_index: int) -> bool:
        return self._hover_delete_idx == log_index

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
        item = self.itemAt(pos)
        new_hover = None
        if item is not None:
            idx_in_logs = item.data(Qt.ItemDataRole.UserRole + 1)
            try:
                idx_in_logs = int(idx_in_logs)
            except Exception:
                idx_in_logs = None
            delegate = self.itemDelegate()
            if isinstance(delegate, LogEntryDelegate) and idx_in_logs is not None:
                rect = self.visualItemRect(item)
                base = rect.adjusted(6, 6, -6, -6)
                w = base.width()
                pad_x = 12 if w >= 520 else (10 if w >= 420 else (8 if w >= 320 else 6))
                del_rect = delegate._delete_rect(base, pad_x)
                if del_rect.contains(pos):
                    new_hover = idx_in_logs

        if new_hover != self._hover_delete_idx:
            self._hover_delete_idx = new_hover
            self.viewport().setCursor(Qt.CursorShape.PointingHandCursor if new_hover is not None else Qt.CursorShape.ArrowCursor)
            self.viewport().update()

        return super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self._hover_delete_idx is not None:
            self._hover_delete_idx = None
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            self.viewport().update()
        return super().leaveEvent(event)

    def mousePressEvent(self, event):
        pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
        item = self.itemAt(pos)
        if item is None:
            return super().mousePressEvent(event)

        data = item.data(Qt.ItemDataRole.UserRole)
        idx_in_logs = item.data(Qt.ItemDataRole.UserRole + 1)
        try:
            idx_in_logs = int(idx_in_logs)
        except Exception:
            idx_in_logs = None

        delegate = self.itemDelegate()
        if isinstance(delegate, LogEntryDelegate) and isinstance(data, dict) and idx_in_logs is not None:
            rect = self.visualItemRect(item)
            base = rect.adjusted(6, 6, -6, -6)
            w = base.width()
            pad_x = 12 if w >= 520 else (10 if w >= 420 else (8 if w >= 320 else 6))
            del_rect = delegate._delete_rect(base, pad_x)
            if del_rect.contains(pos):
                self.deleteRequested.emit(idx_in_logs)
                event.accept()
                return

        return super().mousePressEvent(event)


