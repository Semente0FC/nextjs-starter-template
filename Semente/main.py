import sys
import logging
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from config.config_manager import ConfigManager
from hotkey.hotkey_manager import HotkeyManager
from tray.system_tray import SystemTray
from utils.logger import setup_logger

def main():
    # Setup logger
    logger = setup_logger()
    logger.info("Starting Semente application")

    # Load configuration
    config = ConfigManager()
    try:
        config.load_config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")

    # Create Qt application
    app = QApplication(sys.argv)

    # Create main window
    main_window = MainWindow(config)
    main_window.show()

    # Setup hotkey manager
    hotkey_manager = HotkeyManager(config, main_window)
    hotkey_manager.register_hotkey()

    # Setup system tray
    tray = SystemTray(app, main_window, config)
    tray.setup_tray()

    # Run application event loop
    try:
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"Application crashed: {e}")

if __name__ == "__main__":
    main()
