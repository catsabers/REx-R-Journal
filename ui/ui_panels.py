
from __future__ import annotations

from typing import Dict, List, Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
)

from ore_data import Ore, OreDatabase
from .ui_theme import UiTheme, norm_variant, track_key, variant_color, VARIANTS


class FilterPanel(QWidget):
    changed = Signal()
    exportRequested = Signal()
    importRequested = Signal()
    patchNotesRequested = Signal()
    updateRequested = Signal()

    def __init__(self, ore_db: OreDatabase, parent: QWidget | None = None):
        super().__init__(parent)
        self.ore_db = ore_db
        self.setObjectName("Panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        title = QLabel("Filters")
        title.setStyleSheet("font-size: 16pt; font-weight: 800;")
        layout.addWidget(title)

        self.world = QComboBox()
        self.world.addItems(self.ore_db.get_worlds())
        layout.addWidget(QLabel("World"))
        layout.addWidget(self.world)

        self.layer = QComboBox()
        layout.addWidget(QLabel("Layer"))
        layout.addWidget(self.layer)

        self.cave_only = QCheckBox("Cave exclusive only")
        layout.addWidget(self.cave_only)

        self.cave_type = QComboBox()
        layout.addWidget(QLabel("Cave type"))
        layout.addWidget(self.cave_type)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search ores…")
        layout.addWidget(QLabel("Search"))
        layout.addWidget(self.search)

        self.sort = QComboBox()
        self.sort.addItems(
            [
                "World → Layer",
                "Name (A-Z)",
                "Name (Z-A)",
                "Tier (Rarest First)",
                "Tier (Common First)",
                "Status (Found First)",
                "Status (Not Found First)",
            ]
        )
        layout.addWidget(QLabel("Sort by"))
        layout.addWidget(self.sort)

        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.data_card = QFrame()
        self.data_card.setObjectName("DataCard")
        data_layout = QVBoxLayout(self.data_card)
        data_layout.setContentsMargins(12, 12, 12, 12)
        data_layout.setSpacing(10)

        self.patch_notes_btn = QPushButton("Patch notes")
        self.patch_notes_btn.setObjectName("DataBtn")
        self.patch_notes_btn.setMinimumHeight(38)
        data_layout.addWidget(self.patch_notes_btn)

        self.update_btn = QPushButton("Check for updates")
        self.update_btn.setObjectName("DataBtn")
        self.update_btn.setMinimumHeight(38)
        data_layout.addWidget(self.update_btn)

        data_row = QHBoxLayout()
        data_row.setContentsMargins(0, 0, 0, 0)
        data_row.setSpacing(10)
        self.export_btn = QPushButton("Export…")
        self.import_btn = QPushButton("Import…")
        self.export_btn.setObjectName("DataBtn")
        self.import_btn.setObjectName("DataBtn")
        self.export_btn.setMinimumHeight(38)
        self.import_btn.setMinimumHeight(38)
        data_row.addWidget(self.export_btn, 1)
        data_row.addWidget(self.import_btn, 1)
        data_layout.addLayout(data_row)

        layout.addWidget(self.data_card)

        self.world.currentTextChanged.connect(self._on_world_changed)
        self.layer.currentTextChanged.connect(lambda _v: self.changed.emit())
        self.cave_only.stateChanged.connect(lambda _v: self.changed.emit())
        self.cave_type.currentTextChanged.connect(lambda _v: self.changed.emit())
        self.search.textChanged.connect(lambda _v: self.changed.emit())
        self.sort.currentTextChanged.connect(lambda _v: self.changed.emit())
        self.export_btn.clicked.connect(lambda _v: self.exportRequested.emit())
        self.import_btn.clicked.connect(lambda _v: self.importRequested.emit())
        self.patch_notes_btn.clicked.connect(lambda _v: self.patchNotesRequested.emit())
        self.update_btn.clicked.connect(lambda _v: self.updateRequested.emit())

        self._on_world_changed(self.world.currentText())

    def _on_world_changed(self, world: str):
        self.layer.blockSignals(True)
        self.layer.clear()
        self.layer.addItem("All")
        for layer in self.ore_db.get_layers(world):
            self.layer.addItem(layer)
        self.layer.blockSignals(False)

        self.cave_type.blockSignals(True)
        self.cave_type.clear()
        self.cave: List[str] = self.ore_db.get_cave_types(world)
        self.cave_type.addItem("All")
        for t in self.cave:
            self.cave_type.addItem(t)
        self.cave_type.blockSignals(False)

        self.changed.emit()

    def get_filters(self) -> dict:
        world = self.world.currentText().strip() or None
        layer = self.layer.currentText().strip()
        cave_type = self.cave_type.currentText().strip()
        return {
            "world": world,
            "layer": None if layer == "All" else layer,
            "cave_only": True if self.cave_only.isChecked() else None,
            "cave_type": None if cave_type == "All" else cave_type,
            "search": (self.search.text() or "").strip(),
            "sort": self.sort.currentText(),
        }


class StatsPanel(QWidget):
    def __init__(self, ore_db: OreDatabase, theme: UiTheme, parent: QWidget | None = None):
        super().__init__(parent)
        self.ore_db = ore_db
        self.theme = theme
        self.setObjectName("Panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        self.title_label = QLabel("Stats")
        self.title_label.setStyleSheet("font-size: 16pt; font-weight: 800;")
        layout.addWidget(self.title_label)

        overall_card = QFrame()
        overall_card.setObjectName("WorldCard")
        overall_layout = QVBoxLayout(overall_card)
        overall_layout.setContentsMargins(14, 12, 14, 12)
        overall_layout.setSpacing(8)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        self.overall_pct = QLabel("0.0%")
        self.overall_pct.setStyleSheet("font-size: 30pt; font-weight: 950;")
        top_row.addWidget(self.overall_pct)

        top_row.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.overall_count = QLabel("0 / 0 ores")
        self.overall_count.setObjectName("WorldMeta")
        top_row.addWidget(self.overall_count)

        overall_layout.addLayout(top_row)

        self.overall_bar = QProgressBar()
        self.overall_bar.setRange(0, 1000)
        self.overall_bar.setTextVisible(False)
        self.overall_bar.setFixedHeight(14)
        overall_layout.addWidget(self.overall_bar)

        layout.addWidget(overall_card)

        wp = QLabel("World progress")
        wp.setStyleSheet("font-weight: 800;")
        layout.addWidget(wp)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        try:
            self.scroll.viewport().setStyleSheet("background: transparent;")
        except Exception:
            pass
        layout.addWidget(self.scroll, 1)

        self.world_container = QWidget()
        self.world_container.setStyleSheet("background: transparent;")
        self.world_layout = QVBoxLayout(self.world_container)
        self.world_layout.setContentsMargins(0, 0, 0, 0)
        self.world_layout.setSpacing(10)
        self.scroll.setWidget(self.world_container)

        self._world_rows: Dict[str, QFrame] = {}

        self._cave_card = self._make_world_card("Cave Exclusive")
        self.world_layout.addWidget(self._cave_card)

        self.world_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    @staticmethod
    def _rgba(c: QColor, alpha: float) -> str:
        a = max(0.0, min(1.0, float(alpha)))
        return f"rgba({c.red()},{c.green()},{c.blue()},{a:.3f})"

    def _make_world_card(self, world: str) -> QFrame:
        card = QFrame()
        card.setObjectName("WorldCard")
        card.setProperty("world", world)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 12, 14, 12)
        card_layout.setSpacing(8)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)

        name = QLabel(world)
        name.setObjectName("WorldName")
        row.addWidget(name)

        row.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        meta = QLabel("0/0")
        meta.setObjectName("WorldMeta")
        meta.setProperty("role", "meta")
        row.addWidget(meta)

        pct = QLabel("0.0%")
        pct.setObjectName("WorldPct")
        pct.setProperty("role", "pct")
        row.addWidget(pct)

        card_layout.addLayout(row)

        bar = QProgressBar()
        bar.setRange(0, 1000)
        bar.setTextVisible(False)
        bar.setFixedHeight(12)
        bar.setProperty("role", "bar")
        card_layout.addWidget(bar)

        card._meta_label = meta
        card._pct_label = pct
        card._bar = bar

        return card

    def update(self, all_ores: List[Ore], tracked: Dict[str, bool], variant: str) -> None:
        variant = norm_variant(variant)
        total = len(all_ores)
        found = sum(1 for o in all_ores if tracked.get(track_key(variant, o.key), False))
        pct = (found / total * 100.0) if total else 0.0
        pretty = next((lbl for k, lbl, _c in VARIANTS if k == variant), "Normal")
        self.title_label.setText(f"Stats — {pretty}")
        self.overall_pct.setText(f"{pct:.1f}%")
        self.overall_bar.setValue(int(pct * 10))
        self.overall_count.setText(f"{found} / {total} ores")
        accent = variant_color(variant)
        self.overall_pct.setStyleSheet(f"font-size: 30pt; font-weight: 950; color: {accent.name()};")
        self.overall_bar.setStyleSheet(
            f"""
            QProgressBar::chunk {{
                background: {accent.name()};
                border-radius: 8px;
            }}
            """
        )

        try:
            cave_ores = [o for o in all_ores if bool(getattr(o, "is_cave_exclusive", False))]
        except Exception:
            cave_ores = []
        cave_total = len(cave_ores)
        cave_found = sum(1 for o in cave_ores if tracked.get(track_key(variant, o.key), False))
        cave_pctw = int((cave_found / cave_total * 1000) if cave_total else 0)
        cave_card = getattr(self, "_cave_card", None)
        if cave_card is not None:
            meta = getattr(cave_card, "_meta_label", None)
            pct_label = getattr(cave_card, "_pct_label", None)
            bar = getattr(cave_card, "_bar", None)
            if meta is not None:
                meta.setText(f"{cave_found}/{cave_total}")
            if pct_label is not None:
                pct_label.setText(f"{cave_pctw/10:.1f}%")
                pct_label.setStyleSheet(f"font-weight: 900; color: {accent.name()};")
            if bar is not None:
                bar.setValue(cave_pctw)
                bar.setStyleSheet(
                    f"""
                    QProgressBar::chunk {{
                        background: {accent.name()};
                        border-radius: 8px;
                    }}
                    """
                )
            cave_card.setStyleSheet(
                f"""
                QFrame#WorldCard {{
                    background: {self.theme.card.name()};
                    border: 1px solid {self.theme.border.name()};
                    border-left: 4px solid {self._rgba(accent, 0.65)};
                    border-radius: 14px;
                }}
                """
            )

        world_stats: Dict[str, Tuple[int, int]] = {}
        for o in all_ores:
            t, f = world_stats.get(o.world, (0, 0))
            t += 1
            if tracked.get(track_key(variant, o.key), False):
                f += 1
            world_stats[o.world] = (t, f)

        for w in list(self._world_rows.keys()):
            if w not in world_stats:
                card = self._world_rows.pop(w)
                card.deleteLater()

        desired_order = [w for w in self.ore_db.get_worlds() if w in world_stats]
        for w in desired_order:
            t, f = world_stats[w]
            pctw = int((f / t * 1000) if t else 0)
            if w not in self._world_rows:
                card = self._make_world_card(w)
                insert_at = -1
                try:
                    insert_at = self.world_layout.indexOf(getattr(self, "_cave_card", None))
                except Exception:
                    insert_at = -1
                if insert_at is None or int(insert_at) < 0:
                    insert_at = self.world_layout.count() - 1
                self.world_layout.insertWidget(int(insert_at), card)
                self._world_rows[w] = card

            card = self._world_rows[w]

            meta = getattr(card, "_meta_label", None)
            pct_label = getattr(card, "_pct_label", None)
            bar = getattr(card, "_bar", None)

            if meta is not None:
                meta.setText(f"{f}/{t}")
            if pct_label is not None:
                pct_label.setText(f"{pctw/10:.1f}%")
                pct_label.setStyleSheet(f"font-weight: 900; color: {accent.name()};")
            if bar is not None:
                bar.setValue(pctw)
                bar.setStyleSheet(
                    f"""
                    QProgressBar::chunk {{
                        background: {accent.name()};
                        border-radius: 8px;
                    }}
                    """
                )

            card.setStyleSheet(
                f"""
                QFrame#WorldCard {{
                    background: {self.theme.card.name()};
                    border: 1px solid {self.theme.border.name()};
                    border-left: 4px solid {self._rgba(accent, 0.65)};
                    border-radius: 14px;
                }}
                """
            )


