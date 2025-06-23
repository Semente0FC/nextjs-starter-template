from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QPen

class OverlayWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.opacity_value = 0.0
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)  # 800 ms fade-in
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)

        self.resize(200, 200)
        self.center_on_screen()

        self.crosshair_type = "Cross"
        self.color = QColor("#7F00FF")
        self.thickness = 2
        self.size = 20
        self.opacity = 0.8

        self.load_settings()

    def load_settings(self):
        crosshair = self.config.get_setting("crosshair")
        if crosshair:
            self.crosshair_type = crosshair.get("type", "Cross")
            self.color = QColor(crosshair.get("color", "#7F00FF"))
            self.thickness = crosshair.get("thickness", 2)
            self.size = crosshair.get("size", 20)
            self.opacity = crosshair.get("opacity", 0.8)
        self.setWindowOpacity(self.opacity)

    def center_on_screen(self):
        screen = self.screen()
        if screen:
            geometry = screen.geometry()
            x = geometry.x() + (geometry.width() - self.width()) // 2
            y = geometry.y() + (geometry.height() - self.height()) // 2
            self.move(x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self.opacity)
        pen = QPen(self.color)
        pen.setWidth(self.thickness)
        painter.setPen(pen)

        center_x = self.width() // 2
        center_y = self.height() // 2
        size = self.size

        if self.crosshair_type == "Point":
            painter.drawPoint(center_x, center_y)
        elif self.crosshair_type == "Cross":
            painter.drawLine(center_x - size, center_y, center_x + size, center_y)
            painter.drawLine(center_x, center_y - size, center_x, center_y + size)
        elif self.crosshair_type == "Circle":
            painter.drawEllipse(center_x - size, center_y - size, size * 2, size * 2)
        elif self.crosshair_type == "Square":
            painter.drawRect(center_x - size, center_y - size, size * 2, size * 2)
        else:
            painter.drawLine(center_x - size, center_y, center_x + size, center_y)
            painter.drawLine(center_x, center_y - size, center_x, center_y + size)

    def fade_in(self):
        self.animation.stop()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(self.opacity)
        self.animation.start()
        self.show()

    def update_crosshair(self, crosshair_settings):
        self.crosshair_type = crosshair_settings.get("type", self.crosshair_type)
        self.color = QColor(crosshair_settings.get("color", self.color.name()))
        self.thickness = crosshair_settings.get("thickness", self.thickness)
        self.size = crosshair_settings.get("size", self.size)
        self.opacity = crosshair_settings.get("opacity", self.opacity)
        self.setWindowOpacity(self.opacity)
        self.update()
