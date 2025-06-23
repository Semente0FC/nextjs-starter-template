import keyboard
import logging

class HotkeyManager:
    def __init__(self, config, main_window):
        self.config = config
        self.main_window = main_window
        self.overlay_window = None
        self.logger = logging.getLogger("Semente.HotkeyManager")
        self.registered_hotkey = None

    def register_hotkey(self):
        hotkey = self.config.get_setting("hotkey")
        if not hotkey:
            self.logger.warning("No hotkey configured.")
            return
        try:
            if self.registered_hotkey:
                keyboard.remove_hotkey(self.registered_hotkey)
            self.registered_hotkey = keyboard.add_hotkey(hotkey, self.toggle_overlay)
            self.logger.info(f"Registered global hotkey: {hotkey}")
        except Exception as e:
            self.logger.error(f"Failed to register hotkey {hotkey}: {e}")

    def toggle_overlay(self):
        if not self.overlay_window:
            # Lazy import to avoid circular dependency
            from ui.overlay_window import OverlayWindow
            self.overlay_window = OverlayWindow(self.config)
        if self.overlay_window.isVisible():
            self.overlay_window.hide()
            self.logger.info("Overlay hidden")
        else:
            self.overlay_window.fade_in()
            self.logger.info("Overlay shown")

    def update_hotkey(self, new_hotkey):
        self.config.set_setting("hotkey", new_hotkey)
        self.register_hotkey()
