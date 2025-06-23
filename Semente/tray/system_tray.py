import pystray
from PIL import Image, ImageDraw
import threading
import logging

class SystemTray:
    def __init__(self, app, main_window, config):
        self.app = app
        self.main_window = main_window
        self.config = config
        self.icon = None
        self.logger = logging.getLogger("Semente.SystemTray")

    def create_image(self, width=64, height=64, color1="#7F00FF", color2="#1C1C1C"):
        # Create a simple purple seed icon
        image = Image.new('RGBA', (width, height), color2)
        draw = ImageDraw.Draw(image)
        # Draw a circle with purple color
        draw.ellipse((width*0.2, height*0.2, width*0.8, height*0.8), fill=color1)
        # Draw a smaller black circle inside
        draw.ellipse((width*0.4, height*0.4, width*0.6, height*0.6), fill=color2)
        return image

    def setup_tray(self):
        image = self.create_image()
        menu = pystray.Menu(
            pystray.MenuItem(
                "Show/Hide UI",
                self.toggle_ui
            ),
            pystray.MenuItem(
                "Toggle Game Ready Mode",
                self.toggle_game_ready_mode
            ),
            pystray.MenuItem(
                "Exit",
                self.exit_app
            )
        )
        self.icon = pystray.Icon("Semente", image, "Semente", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()
        self.logger.info("System tray icon started")

    def toggle_ui(self, icon, item):
        if self.main_window.isVisible():
            self.main_window.hide()
            self.logger.info("Main window hidden via tray")
        else:
            self.main_window.show()
            self.logger.info("Main window shown via tray")

    def toggle_game_ready_mode(self, icon, item):
        current = self.config.get_setting("game_ready_mode")
        new_state = not current
        self.config.set_setting("game_ready_mode", new_state)
        self.logger.info(f"Game Ready Mode set to {new_state}")
        if new_state:
            self.main_window.hide()
        else:
            self.main_window.show()

    def exit_app(self, icon, item):
        self.logger.info("Exiting application via tray")
        self.icon.stop()
        self.app.quit()
