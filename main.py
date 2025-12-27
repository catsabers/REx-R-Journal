   

from pathlib import Path

import sys
from typing import Dict, Tuple

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QStandardPaths

from ore_data import OreDatabase
from persistence import load_state, save_state
from qt_gui import DARK, MainWindow, apply_app_theme
from updater import apply_update_and_restart, is_frozen_exe


def get_resource_path(relative_path: str) -> Path:
                                                                      
    try:
                                                                       
        base_path = Path(sys._MEIPASS)
    except AttributeError:
                                     
        base_path = Path(__file__).parent
    return base_path / relative_path


class OreTrackerApp:
                                
    
    def __init__(self):
                                                                                     
        app_data = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        if not app_data:
                                                                   
            app_data = Path.cwd()
        else:
            app_data = Path(app_data)
        
                                      
        self.data_dir = app_data / "REx-R-Journal"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "ore_tracker.json"
        
        self.ore_db = OreDatabase()
        _theme_name, self.variant, self.tracked_ores, self.logs = load_state(self.data_file, self.ore_db)
    
    def run(self):
                                        
        app = QApplication(sys.argv)
        
                              
        from PySide6.QtGui import QIcon
        icon_path = get_resource_path("assets/rexlogo.png")
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
        
        theme = DARK                 
        apply_app_theme(app, theme)

        def on_state_changed(tracked: Dict[str, bool], variant: str, logs):
            self.tracked_ores = dict(tracked)
            self.variant = variant
            self.logs = list(logs or [])
            save_state(self.data_file, "dark", self.variant, self.tracked_ores, self.ore_db, logs=self.logs)

        window = MainWindow(
            self.ore_db,
            self.tracked_ores,
            theme,
            initial_variant=self.variant,
            initial_logs=self.logs,
            on_state_changed=on_state_changed,
        )
        window.show()
        return app.exec()


def main():
                          
                                                                                
    if len(sys.argv) >= 4 and sys.argv[1] == "--apply-update":
        new_exe = Path(sys.argv[2])
        target_exe = Path(sys.argv[3])
        apply_update_and_restart(new_exe, target_exe)
        return

    if is_frozen_exe():
        try:
            exe = Path(sys.executable)
            backup = exe.with_suffix(exe.suffix + ".old")
            backup.unlink(missing_ok=True)
        except Exception:
            pass

    app = OreTrackerApp()
    app.run()


if __name__ == "__main__":
    main()

