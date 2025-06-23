import json
import os
import logging

class ConfigManager:
    def __init__(self, config_path="config/settings.json"):
        self.config_path = config_path
        self.settings = {
            "crosshair": {
                "type": "Cross",
                "color": "#7F00FF",
                "thickness": 2,
                "size": 20,
                "opacity": 0.8
            },
            "hotkey": "F10",
            "game_ready_mode": False
        }
        self.logger = logging.getLogger("Semente.ConfigManager")

    def load_config(self):
        if not os.path.exists(self.config_path):
            self.logger.info(f"Config file not found at {self.config_path}, creating default config.")
            self.save_config()
            return
        try:
            with open(self.config_path, "r") as f:
                self.settings = json.load(f)
            self.logger.info(f"Config loaded from {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            self.logger.info("Using default settings.")
            self.settings = {
                "crosshair": {
                    "type": "Cross",
                    "color": "#7F00FF",
                    "thickness": 2,
                    "size": 20,
                    "opacity": 0.8
                },
                "hotkey": "F10",
                "game_ready_mode": False
            }

    def save_config(self):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self.settings, f, indent=4)
            self.logger.info(f"Config saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")

    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_config()
