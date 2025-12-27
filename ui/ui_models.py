
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from PySide6.QtCore import QAbstractListModel, QModelIndex, QObject, QRect, QSize, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QFontMetrics, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QListView, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QToolButton, QSizePolicy

from ore_data import Ore, OreDatabase, Tier
from .ui_theme import UiTheme, norm_variant, tier_color, track_key, variant_color, VARIANTS


class Roles:
    ORE = Qt.UserRole + 1
    KEY = Qt.UserRole + 2
    FOUND = Qt.UserRole + 3
    WORLD = Qt.UserRole + 4
    LAYER = Qt.UserRole + 5
    TIER = Qt.UserRole + 6
    CAVE_ONLY = Qt.UserRole + 7
    CAVE_TYPE = Qt.UserRole + 8
    ROW_KIND = Qt.UserRole + 9
    HEADER_TEXT = Qt.UserRole + 10


class RowKind:
    ORE = 0
    HEADER = 1


class OreListModel(QAbstractListModel):
    foundToggled = Signal()

    def __init__(self, ores: List[Ore], tracked: Dict[str, bool], variant: str = "normal", parent: QObject | None = None):
        super().__init__(parent)
        self._ores = ores
        self._tracked = tracked
        self.variant = norm_variant(variant)
        self._rows: List[dict] = []
        self.set_view(self._ores, group_by_layer=False)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        kind = row.get("kind", RowKind.ORE)

        if role == Roles.ROW_KIND:
            return kind
        if kind == RowKind.HEADER:
            if role in (Qt.DisplayRole, Roles.HEADER_TEXT):
                return row.get("text", "")
            return None

        ore: Ore = row["ore"]

        if role in (Qt.DisplayRole,):
            return ore.name
        if role == Roles.ORE:
            return ore
        if role == Roles.KEY:
            return ore.key
        if role == Roles.FOUND:
            return bool(self._tracked.get(track_key(self.variant, ore.key), False))
        if role == Roles.WORLD:
            return ore.world
        if role == Roles.LAYER:
            return ore.layer
        if role == Roles.TIER:
            return ore.tier.value
        if role == Roles.CAVE_ONLY:
            return bool(ore.is_cave_exclusive)
        if role == Roles.CAVE_TYPE:
            return ore.cave_type or ""
        return None

    def set_view(self, ores: List[Ore], *, group_by_layer: bool) -> None:
        self.beginResetModel()
        self._rows = []
        if group_by_layer:
            current_layer = None
            for ore in ores:
                if ore.layer != current_layer:
                    current_layer = ore.layer
                    self._rows.append({"kind": RowKind.HEADER, "text": current_layer})
                self._rows.append({"kind": RowKind.ORE, "ore": ore})
        else:
            self._rows = [{"kind": RowKind.ORE, "ore": o} for o in ores]
        self.endResetModel()

    def set_found(self, row: int, value: bool) -> None:
        if not (0 <= row < len(self._rows)):
            return
        if self._rows[row].get("kind") != RowKind.ORE:
            return
        ore: Ore = self._rows[row]["ore"]
        self._tracked[track_key(self.variant, ore.key)] = bool(value)
        idx = self.index(row, 0)
        self.dataChanged.emit(idx, idx, [Roles.FOUND])
        self.foundToggled.emit()

    def toggle_found(self, row: int) -> None:
        if not (0 <= row < len(self._rows)):
            return
        if self._rows[row].get("kind") != RowKind.ORE:
            return
        ore: Ore = self._rows[row]["ore"]
        current = bool(self._tracked.get(track_key(self.variant, ore.key), False))
        self.set_found(row, not current)


def _build_sort_keys(ore_db: OreDatabase):
    world_order = {w: i for i, w in enumerate(ore_db.get_worlds())}
    layer_order_cache = {w: {layer: i for i, layer in enumerate(ore_db.get_layers(w))} for w in ore_db.get_worlds()}
    tier_order = {
        Tier.LAYER: 0,
        Tier.COMMON: 1,
        Tier.UNCOMMON: 2,
        Tier.RARE: 3,
        Tier.MASTER: 4,
        Tier.SURREAL: 5,
        Tier.MYTHIC: 6,
        Tier.EXQUISITE: 7,
        Tier.TRANSCENDENT: 8,
        Tier.ENIGMATIC: 9,
        Tier.UNFATHOMABLE: 10,
        Tier.OTHERWORLDLY: 11,
        Tier.ZENITH: 12,
        Tier.EXCLUSIVE: 13,
    }
    return world_order, layer_order_cache, tier_order


class OreRowDelegate(QStyledItemDelegate):
    def __init__(self, theme: UiTheme, parent: QObject | None = None):
        super().__init__(parent)
        self.theme = theme
        self.variant = "normal"

        self.font_name = QFont("Segoe UI", 12, QFont.Weight.DemiBold)
        self.font_pill = QFont("Segoe UI", 10, QFont.Weight.Bold)
        self.font_meta = QFont("Segoe UI", 9, QFont.Weight.DemiBold)

        self._name_metrics = QFontMetrics(self.font_name)
        self._pill_metrics = QFontMetrics(self.font_pill)

    def set_theme(self, theme: UiTheme):
        self.theme = theme

    def set_variant(self, variant: str):
        self.variant = norm_variant(variant)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        kind = int(index.data(Roles.ROW_KIND) or RowKind.ORE)
        if kind == RowKind.HEADER:
            return QSize(0, 30)
        return QSize(0, 48)

    @staticmethod
    def _rounded_rect_path(rect: QRect, radius: float) -> QPainterPath:
        p = QPainterPath()
        p.addRoundedRect(rect, radius, radius)
        return p

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.save()
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

            is_hover = bool(option.state & QStyle.StateFlag.State_MouseOver)
            is_selected = bool(option.state & QStyle.StateFlag.State_Selected)
            kind = int(index.data(Roles.ROW_KIND) or RowKind.ORE)

            if kind == RowKind.HEADER:
                text = str(index.data(Roles.HEADER_TEXT) or index.data(Qt.DisplayRole) or "")
                r = option.rect.adjusted(12, 2, -12, -2)
                painter.setPen(QPen(self.theme.border, 1))
                painter.drawLine(r.left(), r.center().y(), r.right(), r.center().y())
                chip_h = 22
                painter.setFont(self.font_meta)
                chip_text = text
                fm = QFontMetrics(self.font_meta)
                chip_w = min(r.width(), fm.horizontalAdvance(chip_text) + 18)
                chip = QRect(r.left(), r.center().y() - chip_h // 2, chip_w, chip_h)
                chip_path = self._rounded_rect_path(chip, chip_h / 2)
                painter.fillPath(chip_path, self.theme.panel)
                painter.setPen(self.theme.fg_muted)
                painter.drawText(chip, Qt.AlignmentFlag.AlignCenter, chip_text)
                return

            found = bool(index.data(Roles.FOUND))
            name = str(index.data(Qt.DisplayRole) or "")
            tier_name = str(index.data(Roles.TIER) or "")
            world_name = str(index.data(Roles.WORLD) or "")
            cave_only = bool(index.data(Roles.CAVE_ONLY))
            cave_type = str(index.data(Roles.CAVE_TYPE) or "").strip()

            r = option.rect.adjusted(10, 4, -10, -4)
            bg = self.theme.card_found if found else (self.theme.card_hover if is_hover else self.theme.card)
            if is_selected:
                bg = bg.lighter(112)

            path = self._rounded_rect_path(r, 14)
            painter.fillPath(path, bg)
            painter.setPen(QPen(self.theme.border, 1))
            painter.drawPath(path)

            cb = QRect(r.left() + 14, r.center().y() - 9, 18, 18)
            painter.setPen(QPen(self.theme.border, 1))
            painter.setBrush(QBrush(QColor("#00000000")))
            painter.drawRoundedRect(cb, 4, 4)
            if found:
                painter.setPen(QPen(self.theme.accent, 2))
                x1, y1 = cb.left() + 4, cb.center().y()
                x2, y2 = cb.left() + 8, cb.bottom() - 5
                x3, y3 = cb.right() - 4, cb.top() + 5
                painter.drawLine(x1, y1, x2, y2)
                painter.drawLine(x2, y2, x3, y3)

            painter.setFont(self.font_name)
            name_x = cb.right() + 12
            name_rect = QRect(name_x, r.top(), r.width() - 260, r.height())
            elided = self._name_metrics.elidedText(name, Qt.TextElideMode.ElideRight, name_rect.width())

            glow = variant_color(self.variant)
            base = QColor(self.theme.fg)
            name_color = QColor(
                int(base.red() * 0.65 + glow.red() * 0.35),
                int(base.green() * 0.65 + glow.green() * 0.35),
                int(base.blue() * 0.65 + glow.blue() * 0.35),
            )

            glow_soft = QColor(glow)
            glow_soft.setAlpha(82 if self.theme.name == "dark" else 56)
            painter.setPen(glow_soft)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                painter.drawText(name_rect.translated(dx, dy), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, elided)

            glow_soft2 = QColor(glow)
            glow_soft2.setAlpha(46 if self.theme.name == "dark" else 32)
            painter.setPen(glow_soft2)
            for dx, dy in [(-2, 0), (2, 0)]:
                painter.drawText(name_rect.translated(dx, dy), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, elided)

            painter.setPen(name_color)
            painter.drawText(name_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, elided)

            right_x = r.right() - 14
            pill_gap = 10

            def draw_pill(text: str, color: QColor, fg: QColor, x_right: int, height: int, border: QColor | None = None) -> int:
                painter.setFont(self.font_pill)
                pad_x = 12
                w = max(78, min(220, self._pill_metrics.horizontalAdvance(text) + pad_x * 2))
                rect = QRect(x_right - w, r.center().y() - height // 2, w, height)
                pill_path = self._rounded_rect_path(rect, height / 2)
                painter.fillPath(pill_path, color)
                if border is not None:
                    painter.setPen(QPen(border, 1))
                    painter.drawPath(pill_path)
                else:
                    painter.setPen(QPen(QColor("#00000000"), 0))
                    painter.drawPath(pill_path)
                painter.setPen(fg)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
                return rect.left() - pill_gap

            if world_name == "Natura" and tier_name == "Zenith":
                tier_bg = QColor("#000000")
                tier_fg = QColor("#ffffff")
                tier_border = QColor("#000000")
                tier_border.setAlpha(200)
            else:
                basec = tier_color(self.theme, tier_name)
                tier_bg = QColor(basec)
                tier_bg.setAlpha(70)
                tier_border = QColor(basec)
                tier_border.setAlpha(170)
                tier_fg = QColor(basec).darker(190) if basec.lightness() > 150 else QColor(basec).lighter(185)
            right_x = draw_pill(tier_name, tier_bg, tier_fg, right_x, 26, border=tier_border)

            if cave_only:
                label = cave_type if cave_type else "Cave"
                cave_bg = self.theme.accent.darker(110)
                _ = draw_pill(label, cave_bg, QColor("#ffffff"), right_x, 22)
        finally:
            painter.restore()


class OreListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setUniformItemSizes(True)
        self.setVerticalScrollMode(QListView.ScrollMode.ScrollPerPixel)
        self.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self.setSpacing(2)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


class VariantGlowButton(QToolButton):
    def __init__(self, variant_key: str, label: str, theme: UiTheme, parent=None):
        super().__init__(parent)
        self.variant_key = norm_variant(variant_key)
        self._theme = theme
        self.setText(label)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(32)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self._font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        self._fm = QFontMetrics(self._font)

    def set_theme(self, theme: UiTheme) -> None:
        self._theme = theme
        self.update()

    def set_variant_key(self, variant_key: str) -> None:
        self.variant_key = norm_variant(variant_key)
        self.update()

    def sizeHint(self) -> QSize:
        pad_x = 18
        w = self._fm.horizontalAdvance(self.text()) + pad_x * 2
        return QSize(max(86, w), 32)

    @staticmethod
    def _blend(a: QColor, b: QColor, t: float) -> QColor:
        t = max(0.0, min(1.0, float(t)))
        return QColor(
            int(a.red() * (1 - t) + b.red() * t),
            int(a.green() * (1 - t) + b.green() * t),
            int(a.blue() * (1 - t) + b.blue() * t),
        )

    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        rect = self.rect().adjusted(1, 1, -1, -1)
        r = 12

        vcol = variant_color(self.variant_key)
        checked = self.isChecked()
        hover = self.underMouse()

        bg = QColor(vcol if checked else self._theme.card_hover)
        bg.setAlpha(60 if checked else (25 if hover else 0))
        border = QColor(vcol if checked else self._theme.border)
        border.setAlpha(140 if checked else (80 if hover else 0))

        path = QPainterPath()
        path.addRoundedRect(rect, r, r)
        if bg.alpha() > 0:
            p.fillPath(path, bg)
        if border.alpha() > 0:
            p.setPen(QPen(border, 1))
            p.drawPath(path)

        p.setFont(self._font)
        text = self.text()
        trect = rect.adjusted(10, 0, -10, 0)

        base = self._theme.fg if checked else self._theme.fg_muted
        name_color = self._blend(base, vcol, 0.60 if checked else 0.40)

        glow1 = QColor(vcol)
        glow1.setAlpha(140 if checked else 70)
        p.setPen(glow1)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            p.drawText(trect.translated(dx, dy), Qt.AlignmentFlag.AlignCenter, text)

        glow2 = QColor(vcol)
        glow2.setAlpha(85 if checked else 40)
        p.setPen(glow2)
        for dx, dy in [(-2, 0), (2, 0)]:
            p.drawText(trect.translated(dx, dy), Qt.AlignmentFlag.AlignCenter, text)

        p.setPen(name_color)
        p.drawText(trect, Qt.AlignmentFlag.AlignCenter, text)

        p.end()


