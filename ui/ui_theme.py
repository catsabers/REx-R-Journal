
from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication


@dataclass(frozen=True)
class UiTheme:
    name: str
    bg: QColor
    panel: QColor
    card: QColor
    card_hover: QColor
    card_found: QColor
    fg: QColor
    fg_muted: QColor
    border: QColor
    accent: QColor


DARK = UiTheme(
    name="dark",
    bg=QColor("#0f1115"),
    panel=QColor("#171a21"),
    card=QColor("#141821"),
    card_hover=QColor("#1a2030"),
    card_found=QColor("#11261c"),
    fg=QColor("#f6f7fb"),
    fg_muted=QColor("#a9b1c3"),
    border=QColor("#2a3142"),
    accent=QColor("#7c5cff"),
)


TIER_COLORS_DARK = {
    "Layer": "#808080",
    "Common": "#E0E0E0",
    "Uncommon": "#4CAF50",
    "Rare": "#2196F3",
    "Master": "#9C27B0",
    "Surreal": "#FF9800",
    "Mythic": "#F44336",
    "Exquisite": "#00FF88",
    "Transcendent": "#00D4FF",
    "Enigmatic": "#FFEB3B",
    "Unfathomable": "#00CED1",
    "Otherworldly": "#DC143C",
    "Zenith": "#FF8C00",
    "Exclusive": "#FF1493",
}


def tier_color(theme: UiTheme, tier_name: str) -> QColor:
    return QColor(TIER_COLORS_DARK.get(tier_name, "#ffffff"))


VARIANTS = [
    ("normal", "Normal", QColor("#00D4FF")),
    ("ionized", "Ionized", QColor("#FFD54A")),
    ("spectral", "Spectral", QColor("#FF4D4D")),
]
VARIANT_SET = {v[0] for v in VARIANTS}


def norm_variant(v: str | None) -> str:
    v = (v or "normal").strip().lower()
    return v if v in VARIANT_SET else "normal"


def variant_color(variant: str) -> QColor:
    vv = norm_variant(variant)
    for k, _label, c in VARIANTS:
        if k == vv:
            return QColor(c)
    return QColor("#00D4FF")


def track_key(variant: str, ore_key: str) -> str:
    return f"{norm_variant(variant)}|{ore_key}"


def apply_app_theme(app: QApplication, theme: UiTheme) -> None:
    brand_bg = "rgba(255,255,255,0.06)" if theme.name == "dark" else "rgba(0,0,0,0.05)"
    v_norm = variant_color("normal")
    v_ion = variant_color("ionized")
    v_spec = variant_color("spectral")
    rgba = lambda c, a: f"rgba({c.red()},{c.green()},{c.blue()},{a})"
    sb_track = "rgba(255,255,255,0.06)" if theme.name == "dark" else "rgba(0,0,0,0.06)"
    sb_handle = "rgba(255,255,255,0.22)" if theme.name == "dark" else "rgba(0,0,0,0.20)"
    sb_handle_hover = "rgba(255,255,255,0.34)" if theme.name == "dark" else "rgba(0,0,0,0.30)"
    sb_handle_pressed = rgba(theme.accent, 0.55)
    app.setStyleSheet(
        f"""
        QWidget {{
            background: {theme.bg.name()};
            color: {theme.fg.name()};
            font-family: "Segoe UI", "Inter", "Arial";
            font-size: 12pt;
        }}
        QLabel {{
            background: transparent;
        }}
        QScrollArea, QAbstractScrollArea, QListView {{
            background: transparent;
        }}
        QScrollBar:vertical {{
            background: transparent;
            width: 12px;
            margin: 10px 4px 10px 4px;
            border-radius: 6px;
        }}
        QScrollBar::groove:vertical {{
            background: {sb_track};
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {sb_handle};
            border-radius: 6px;
            min-height: 28px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {sb_handle_hover};
        }}
        QScrollBar::handle:vertical:pressed {{
            background: {sb_handle_pressed};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
            background: transparent;
            border: none;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: transparent;
        }}

        QScrollBar:horizontal {{
            background: transparent;
            height: 12px;
            margin: 4px 10px 4px 10px;
            border-radius: 6px;
        }}
        QScrollBar::groove:horizontal {{
            background: {sb_track};
            border-radius: 6px;
        }}
        QScrollBar::handle:horizontal {{
            background: {sb_handle};
            border-radius: 6px;
            min-width: 28px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {sb_handle_hover};
        }}
        QScrollBar::handle:horizontal:pressed {{
            background: {sb_handle_pressed};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
            background: transparent;
            border: none;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: transparent;
        }}
        QMainWindow::separator {{ background: {theme.border.name()}; }}
        QFrame#Header {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {theme.panel.name()},
                stop:1 {theme.card_hover.name()}
            );
            border-bottom: 1px solid {theme.border.name()};
            border-radius: 16px;
        }}
        QFrame#Header QWidget {{
            background: transparent;
        }}
        QFrame#Brand {{
            background: {brand_bg};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QFrame#NavToggle {{
            background: {brand_bg};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QToolButton#NavBtn {{
            background: transparent;
            border: none;
            border-radius: 12px;
            padding: 8px 12px;
            font-weight: 900;
            color: {theme.fg_muted.name()};
        }}
        QToolButton#NavBtn:checked {{
            background: {theme.card_hover.name()};
            color: {theme.fg.name()};
        }}
        QListWidget {{
            background: transparent;
            border: none;
            outline: none;
        }}
        QListWidget::item {{
            background: {theme.card.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 12px;
            padding: 10px 12px;
            margin: 4px 2px;
        }}
        QListWidget::item:selected {{
            background: {theme.card_hover.name()};
        }}
        QFrame#LogBox {{
            background: {theme.card.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QFrame#DialogCard {{
            background: {theme.card.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QFrame#DialogListBox {{
            background: {theme.panel.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QFrame#DialogDetails {{
            background: {theme.card.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QLabel#DialogSectionTitle {{
            font-weight: 900;
            color: {theme.fg.name()};
        }}
        QCalendarWidget QWidget {{
            background: {theme.panel.name()};
            color: {theme.fg.name()};
        }}
        QCalendarWidget QToolButton {{
            background: {theme.card_hover.name()};
            color: {theme.fg.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 10px;
            padding: 6px 10px;
            font-weight: 800;
        }}
        QCalendarWidget QToolButton:hover {{
            background: {theme.card_hover.lighter(110).name()};
        }}
        QCalendarWidget QMenu {{
            background: {theme.panel.name()};
            border: 1px solid {theme.border.name()};
        }}
        QCalendarWidget QSpinBox {{
            background: {theme.card.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 10px;
            padding: 4px 8px;
        }}
        QCalendarWidget QAbstractItemView {{
            selection-background-color: {rgba(theme.accent, 0.35)};
            selection-color: {theme.fg.name()};
            background: {theme.panel.name()};
            border: none;
        }}
        QWidget#Panel {{
            background: {theme.panel.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QFrame#WorldCard {{
            background: {theme.card.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QLabel#WorldName {{
            font-weight: 800;
        }}
        QLabel#WorldMeta {{
            color: {theme.fg_muted.name()};
            font-weight: 700;
        }}
        QLabel#WorldPct {{
            font-weight: 900;
        }}
        QLineEdit, QComboBox {{
            background: {theme.card.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 10px;
            padding: 8px 10px;
        }}
        QDateEdit {{
            background: {theme.card.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 10px;
            padding: 8px 10px;
            padding-right: 34px;
        }}
        QComboBox::drop-down {{
            border: none;
            width: 28px;
        }}
        QDateEdit::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 28px;
            border: none;
            background: {theme.card_hover.name()};
            border-left: 1px solid {theme.border.name()};
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
        }}
        QDateEdit::down-arrow {{
            width: 10px;
            height: 10px;
        }}
        QComboBox QAbstractItemView {{
            background: {theme.panel.name()};
            border: 1px solid {theme.border.name()};
            selection-background-color: {theme.card_hover.name()};
        }}
        QPushButton, QToolButton {{
            background: {theme.accent.name()};
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 8px 12px;
            font-weight: 600;
        }}
        QPushButton:hover, QToolButton:hover {{
            background: {theme.accent.lighter(115).name()};
        }}

        QFrame#DataCard {{
            background: {brand_bg};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QPushButton#DataBtn {{
            background: {theme.card_hover.name()};
            color: {theme.fg.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 12px;
            padding: 10px 12px;
            font-weight: 800;
        }}
        QPushButton#DataBtn:hover {{
            background: {theme.card_hover.lighter(112).name()};
        }}
        QFrame#VariantToggle {{
            background: {brand_bg};
            border: 1px solid {theme.border.name()};
            border-radius: 14px;
        }}
        QToolButton#VariantBtn {{
            background: transparent;
            border: none;
            border-radius: 12px;
            padding: 8px 12px;
            font-weight: 800;
            color: {theme.fg_muted.name()};
        }}
        QProgressBar {{
            background: {theme.card.name()};
            border: 1px solid {theme.border.name()};
            border-radius: 8px;
            height: 14px;
            text-align: center;
        }}
        QProgressBar::chunk {{
            background: {theme.accent.name()};
            border-radius: 8px;
        }}
        """
    )


