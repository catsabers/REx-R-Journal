
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Dict

from PySide6.QtCore import QModelIndex, QObject, Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressDialog,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)

from app_meta import CURRENT_VERSION, GITHUB_REPO
from ore_data import Ore, OreDatabase
from persistence import load_state_from_obj, save_state
import updater
from .ui_log import LogEntryDelegate, LogFindDialog, LogListWidget
from .ui_models import OreListModel, OreListView, OreRowDelegate, VariantGlowButton, _build_sort_keys
from .ui_panels import FilterPanel, StatsPanel
from .ui_theme import UiTheme, norm_variant, track_key, variant_color, VARIANTS


class MainWindow(QMainWindow):
    def __init__(
        self,
        ore_db: OreDatabase,
        tracked: Dict[str, bool],
        theme: UiTheme,
        initial_variant: str,
        initial_logs,
        on_state_changed,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.ore_db = ore_db
        self.tracked = tracked
        self.theme = theme
        self.variant = norm_variant(initial_variant)
        self._on_state_changed = on_state_changed
        self.logs = list(initial_logs or [])

        self.setWindowTitle("REx:R Journal")

        def get_resource_path(relative_path: str) -> Path:
            try:
                base_path = Path(sys._MEIPASS)
            except AttributeError:
                base_path = Path(__file__).parent
            return base_path / relative_path

        icon_path = get_resource_path("assets/rexlogo.png")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.resize(1400, 820)

        FILTER_W = 320
        STATS_W = 360
        CENTER_MIN_W = 520
        BODY_SPACING = 12 * 2
        OUTER_MARGINS = 14 * 2
        min_w = FILTER_W + CENTER_MIN_W + STATS_W + BODY_SPACING + OUTER_MARGINS
        self.setMinimumWidth(min_w)
        self.setMinimumHeight(720)

        header = QFrame()
        header.setObjectName("Header")
        header.setFixedHeight(72)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 10, 16, 10)
        header_layout.setSpacing(14)

        brand = QFrame()
        brand.setObjectName("Brand")
        brand_layout = QHBoxLayout(brand)
        brand_layout.setContentsMargins(14, 8, 14, 8)
        brand_layout.setSpacing(10)

        title = QLabel("REx:R Journal")
        title.setStyleSheet("font-size: 18pt; font-weight: 900; letter-spacing: 0.5px;")
        brand_layout.addWidget(title)

        header_layout.addWidget(brand)

        nav = QFrame()
        nav.setObjectName("NavToggle")
        nav_layout = QHBoxLayout(nav)
        nav_layout.setContentsMargins(6, 6, 6, 6)
        nav_layout.setSpacing(4)
        self._nav_group = QButtonGroup(self)
        self._nav_group.setExclusive(True)

        self.index_btn = QToolButton()
        self.index_btn.setObjectName("NavBtn")
        self.index_btn.setText("Index")
        self.index_btn.setCheckable(True)
        self.index_btn.setChecked(True)
        self._nav_group.addButton(self.index_btn)
        nav_layout.addWidget(self.index_btn)

        self.log_btn = QToolButton()
        self.log_btn.setObjectName("NavBtn")
        self.log_btn.setText("Log")
        self.log_btn.setCheckable(True)
        self._nav_group.addButton(self.log_btn)
        nav_layout.addWidget(self.log_btn)

        header_layout.addWidget(nav)

        header_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        variant_frame = QFrame()
        variant_frame.setObjectName("VariantToggle")
        variant_layout = QHBoxLayout(variant_frame)
        variant_layout.setContentsMargins(6, 6, 6, 6)
        variant_layout.setSpacing(4)

        self._variant_group = QButtonGroup(self)
        self._variant_group.setExclusive(True)
        self._variant_buttons: Dict[str, VariantGlowButton] = {}

        for key, label, _c in VARIANTS:
            btn = VariantGlowButton(key, label, theme=self.theme)
            self._variant_group.addButton(btn)
            self._variant_buttons[key] = btn
            variant_layout.addWidget(btn)

        self._variant_buttons.get(self.variant, self._variant_buttons["normal"]).setChecked(True)
        self._variant_group.buttonClicked.connect(self._on_variant_changed)

        header_layout.addWidget(variant_frame)

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(14, 14, 14, 14)
        root_layout.setSpacing(12)
        root_layout.addWidget(header)

        self.pages = QStackedWidget()
        root_layout.addWidget(self.pages, 1)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(12)
        self.pages.addWidget(body)

        self.filter_panel = FilterPanel(self.ore_db)
        self.filter_panel.setFixedWidth(320)
        body_layout.addWidget(self.filter_panel)

        self.ore_model = OreListModel([], self.tracked, variant=self.variant)
        self._world_order, self._layer_order_cache, self._tier_order = _build_sort_keys(self.ore_db)

        self.list_view = OreListView()
        self.list_view.setModel(self.ore_model)
        self.list_view.setMinimumWidth(CENTER_MIN_W)
        self.delegate = OreRowDelegate(self.theme, self.list_view)
        self.delegate.set_variant(self.variant)
        self.list_view.setItemDelegate(self.delegate)
        body_layout.addWidget(self.list_view, 1)

        self.stats_panel = StatsPanel(self.ore_db, theme=self.theme)
        self.stats_panel.setFixedWidth(360)
        body_layout.addWidget(self.stats_panel)

        log_page = QWidget()
        log_layout = QVBoxLayout(log_page)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.setSpacing(12)

        log_header = QHBoxLayout()
        log_header.setContentsMargins(0, 0, 0, 0)
        log_header.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.log_find_btn = QPushButton("Log Find")
        self.log_find_btn.setMinimumWidth(160)
        log_header.addWidget(self.log_find_btn)
        log_header.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        log_layout.addLayout(log_header)

        log_box = QFrame()
        log_box.setObjectName("LogBox")
        log_box_layout = QVBoxLayout(log_box)
        log_box_layout.setContentsMargins(10, 10, 10, 10)
        log_box_layout.setSpacing(8)

        self.log_list = LogListWidget()
        self.log_list.setItemDelegate(LogEntryDelegate(self.theme, parent=self.log_list))
        self.log_list.setStyleSheet("QListWidget::item{background:transparent;border:none;margin:0;padding:0;}")
        self.log_list.setSpacing(8)
        self.log_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        log_box_layout.addWidget(self.log_list, 1)

        log_layout.addWidget(log_box, 1)
        self.pages.addWidget(log_page)

        self.setCentralWidget(root)

        self.filter_panel.changed.connect(self._apply_filters)
        self.filter_panel.exportRequested.connect(self._export_data)
        self.filter_panel.importRequested.connect(self._import_data)
        self.filter_panel.updateRequested.connect(self._check_for_updates)
        self.list_view.clicked.connect(self._on_click)
        self.ore_model.foundToggled.connect(self._refresh_stats_and_save)
        self._nav_group.buttonClicked.connect(self._on_nav_changed)
        self.log_find_btn.clicked.connect(self._open_log_find)
        self.log_list.deleteRequested.connect(self._delete_log_entry)

        self._apply_filters()
        self._refresh_stats_and_save(save=False)
        self._refresh_log_list()

    def _apply_filters(self):
        f = self.filter_panel.get_filters()
        filtered = self.ore_db.filter_ores(
            world=f["world"],
            layer=f["layer"],
            is_cave_exclusive=f["cave_only"],
            cave_type=f["cave_type"],
            search_term=f["search"],
        )

        sort_mode = f["sort"] or "World → Layer"

        def tier_rank(ore: Ore) -> int:
            return self._tier_order.get(ore.tier, 999)

        def layer_rank(ore: Ore) -> int:
            return self._layer_order_cache.get(ore.world, {}).get(ore.layer, 999)

        def world_rank(ore: Ore) -> int:
            return self._world_order.get(ore.world, 999)

        if sort_mode == "Name (A-Z)":
            sorted_ores = sorted(filtered, key=lambda o: o.name.lower())
        elif sort_mode == "Name (Z-A)":
            sorted_ores = sorted(filtered, key=lambda o: o.name.lower(), reverse=True)
        elif sort_mode == "Tier (Rarest First)":
            sorted_ores = sorted(filtered, key=lambda o: (-tier_rank(o), o.name.lower()))
        elif sort_mode == "Tier (Common First)":
            sorted_ores = sorted(filtered, key=lambda o: (tier_rank(o), o.name.lower()))
        elif sort_mode == "Status (Found First)":
            sorted_ores = sorted(filtered, key=lambda o: (not self.tracked.get(track_key(self.variant, o.key), False), o.name.lower()))
        elif sort_mode == "Status (Not Found First)":
            sorted_ores = sorted(filtered, key=lambda o: (self.tracked.get(track_key(self.variant, o.key), False), o.name.lower()))
        else:
            sorted_ores = sorted(filtered, key=lambda o: (world_rank(o), layer_rank(o), tier_rank(o), o.name.lower()))

        group_by_layer = bool(f["world"]) and (f["layer"] is None) and (sort_mode == "World → Layer")
        self.ore_model.set_view(sorted_ores, group_by_layer=group_by_layer)

    def _on_click(self, proxy_index: QModelIndex):
        if not proxy_index.isValid():
            return
        self.ore_model.toggle_found(proxy_index.row())

    def _refresh_stats_and_save(self, save: bool = True):
        self.stats_panel.update(self.ore_db.get_all_ores(), self.tracked, self.variant)
        if save:
            self._on_state_changed(self.tracked, self.variant, self.logs)

    def _on_nav_changed(self, _btn=None):
        self.pages.setCurrentIndex(0 if self.index_btn.isChecked() else 1)

    def _refresh_log_list(self):
        self.log_list.clear()
        ore_map = {o.key: o for o in self.ore_db.get_all_ores()}
        for idx, e in reversed(list(enumerate(self.logs))):
            if not isinstance(e, dict):
                continue
            e2 = dict(e)
            if not e2.get("tier"):
                ok = e2.get("ore_key")
                ore = ore_map.get(str(ok)) if ok else None
                if ore is not None:
                    e2["tier"] = ore.tier.value
            item = QListWidgetItem("")
            item.setData(Qt.ItemDataRole.UserRole, e2)
            item.setData(Qt.ItemDataRole.UserRole + 1, idx)
            self.log_list.addItem(item)

    def _open_log_find(self):
        dlg = LogFindDialog(self.ore_db, self.theme, initial_variant=self.variant, parent=self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        ore_key = dlg.selected_ore_key()
        if not ore_key:
            return

        chosen = next((o for o in self.ore_db.get_all_ores() if o.key == ore_key), None)
        if chosen is None:
            return

        date_iso = dlg.selected_date_iso()
        entry_variant = dlg.selected_variant()
        mined = dlg.selected_mined()

        self.tracked[track_key(entry_variant, chosen.key)] = True

        self.logs.append(
            {
                "date": date_iso,
                "variant": entry_variant,
                "ore_key": chosen.key,
                "ore_name": chosen.name,
                "world": chosen.world,
                "layer": chosen.layer,
                "mined": mined,
            }
        )

        self._apply_filters()
        self._refresh_log_list()
        self._refresh_stats_and_save(save=True)

    def _delete_log_entry(self, log_index: int):
        if not isinstance(log_index, int):
            return
        if not (0 <= log_index < len(self.logs)):
            return
        try:
            self.logs.pop(log_index)
        except Exception:
            return
        self._refresh_log_list()
        self._refresh_stats_and_save(save=True)

    def _on_variant_changed(self, _btn=None):
        for key, btn in self._variant_buttons.items():
            if btn.isChecked():
                self.variant = norm_variant(key)
                break
        self.ore_model.variant = self.variant
        self.delegate.set_variant(self.variant)
        self._apply_filters()
        self._refresh_stats_and_save(save=True)

    def _export_data(self):
        default_name = "REx-R-Journal-export.json"
        path, _selected = QFileDialog.getSaveFileName(
            self,
            "Export Progress",
            default_name,
            "JSON Files (*.json);;All Files (*.*)",
        )
        if not path:
            return

        try:
            save_state(Path(path), "dark", self.variant, self.tracked, self.ore_db, logs=self.logs)
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Could not export.\n\n{e}")
            return

        QMessageBox.information(self, "Export Complete", f"Exported to:\n{path}")

    def _import_data(self):
        path, _selected = QFileDialog.getOpenFileName(
            self,
            "Import Progress",
            "",
            "JSON Files (*.json);;All Files (*.*)",
        )
        if not path:
            return

        confirm = QMessageBox.question(
            self,
            "Import Progress",
            "Importing will replace your current tracked ores and log entries.\n\nContinue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            raw = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception as e:
            QMessageBox.critical(self, "Import Failed", f"That file is not valid JSON.\n\n{e}")
            return

        try:
            _theme, imported_variant, imported_tracked, imported_logs = load_state_from_obj(raw, self.ore_db)
        except Exception as e:
            QMessageBox.critical(self, "Import Failed", f"Could not parse import file.\n\n{e}")
            return

        self.tracked.clear()
        self.tracked.update(dict(imported_tracked or {}))
        self.logs = list(imported_logs or [])

        self.variant = norm_variant(imported_variant)
        btn = self._variant_buttons.get(self.variant)
        if btn is not None:
            btn.setChecked(True)
        else:
            self._variant_buttons["normal"].setChecked(True)
            self.variant = "normal"

        self.ore_model.variant = self.variant
        self.delegate.set_variant(self.variant)
        self._apply_filters()
        self._refresh_log_list()
        self._refresh_stats_and_save(save=True)

        QMessageBox.information(self, "Import Complete", "Import finished. Your progress has been loaded and saved.")

    class _UpdateCheckThread(QThread):
        done = Signal(object, str)

        def __init__(self, repo: str, parent: QObject | None = None):
            super().__init__(parent)
            self.repo = repo

        def run(self) -> None:
            try:
                rel = updater.fetch_latest_release(self.repo)
                self.done.emit(rel, "")
            except Exception as e:
                self.done.emit(None, str(e))

    class _UpdateDownloadThread(QThread):
        progress = Signal(int)
        done = Signal(object, str)

        def __init__(self, url: str, dest: Path, parent: QObject | None = None):
            super().__init__(parent)
            self.url = url
            self.dest = Path(dest)

        def run(self) -> None:
            try:
                updater.download_to_file(
                    self.url,
                    self.dest,
                    progress_cb=lambda p: self.progress.emit(int(p)),
                    cancel_cb=lambda: bool(self.isInterruptionRequested()),
                )
                self.done.emit(self.dest, "")
            except Exception as e:
                self.done.emit(None, str(e))

    @staticmethod
    def _safe_filename(s: str) -> str:
        s = (s or "").strip()
        return "".join(ch if (ch.isalnum() or ch in ".-_") else "_" for ch in s)[:140] or "download"

    def _check_for_updates(self):
        try:
            self.filter_panel.update_btn.setEnabled(False)
            self.filter_panel.update_btn.setText("Checking…")
        except Exception:
            pass

        busy = QProgressDialog("Checking for updates…", "Cancel", 0, 0, self)
        busy.setWindowModality(Qt.WindowModality.WindowModal)
        busy.setAutoClose(True)
        busy.setAutoReset(True)
        busy.setMinimumDuration(0)
        busy.show()

        t = MainWindow._UpdateCheckThread(GITHUB_REPO, parent=self)
        self._update_check_thread = t

        def _done(release_obj, err: str):
            try:
                busy.close()
            except Exception:
                pass
            try:
                self.filter_panel.update_btn.setEnabled(True)
                self.filter_panel.update_btn.setText("Check for updates")
            except Exception:
                pass

            if err or not release_obj:
                QMessageBox.warning(self, "Update Check Failed", f"Could not check for updates.\n\n{err or 'Unknown error'}")
                return

            release = release_obj
            if not updater.is_newer(getattr(release, "tag_name", ""), CURRENT_VERSION):
                QMessageBox.information(self, "Up to Date", f"You're up to date.\n\nCurrent version: v{CURRENT_VERSION}")
                return

            preferred = None
            if updater.is_frozen_exe():
                try:
                    preferred = Path(sys.executable).name
                except Exception:
                    preferred = None

            asset = updater.choose_windows_exe_asset(release, preferred_name=preferred)
            if asset is None:
                QMessageBox.information(
                    self,
                    "Update Available",
                    f"A new version is available: {release.tag_name}\n\n"
                    f"Couldn't find a Windows .exe asset in that release.\n\n"
                    f"Release page:\n{release.html_url}",
                )
                return

            resp = QMessageBox.question(
                self,
                "Update Available",
                f"A new version is available: {release.tag_name}\n"
                f"Current version: v{CURRENT_VERSION}\n\n"
                "Download and install now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if resp != QMessageBox.StandardButton.Yes:
                return

            self._download_and_install_update(release, asset)

        busy.canceled.connect(lambda: None)
        t.done.connect(_done)
        t.start()

    def _download_and_install_update(self, release, asset):
        tmpdir = Path(tempfile.gettempdir())
        tag = self._safe_filename(getattr(release, "tag_name", "latest"))
        asset_name = self._safe_filename(getattr(asset, "name", "update.exe"))
        dest = tmpdir / f"{Path(asset_name).stem}-{tag}{Path(asset_name).suffix}"

        dlg = QProgressDialog("Downloading update…", "Cancel", 0, 100, self)
        dlg.setWindowModality(Qt.WindowModality.WindowModal)
        dlg.setAutoClose(False)
        dlg.setAutoReset(False)
        dlg.setMinimumDuration(0)
        dlg.setValue(0)
        dlg.show()

        t = MainWindow._UpdateDownloadThread(getattr(asset, "download_url", ""), dest, parent=self)
        self._update_download_thread = t

        def _on_progress(p: int):
            try:
                dlg.setValue(int(p))
            except Exception:
                pass

        def _on_done(path_obj, err: str):
            try:
                dlg.close()
            except Exception:
                pass

            if err or not path_obj:
                QMessageBox.critical(self, "Update Failed", f"Could not download the update.\n\n{err or 'Unknown error'}")
                return

            new_exe = Path(path_obj)
            if not updater.is_frozen_exe():
                QMessageBox.information(
                    self,
                    "Update Downloaded",
                    f"Downloaded update to:\n{new_exe}\n\n"
                    "Auto-install is only supported in the packaged .exe build.\n"
                    f"Release page:\n{getattr(release, 'html_url', '')}",
                )
                return

            current_exe = Path(sys.executable)
            try:
                helper = updater.make_helper_copy(current_exe)
                updater.spawn_apply_update(helper, new_exe, current_exe)
            except Exception as e:
                QMessageBox.critical(self, "Update Failed", f"Could not start updater.\n\n{e}")
                return

            QMessageBox.information(self, "Updating…", "The app will now close to apply the update, then restart.")
            try:
                QApplication.instance().quit()
            except Exception:
                self.close()

        dlg.canceled.connect(lambda: t.requestInterruption())
        t.progress.connect(_on_progress)
        t.done.connect(_on_done)
        t.start()


