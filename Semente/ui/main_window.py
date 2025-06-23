from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QSlider, QPushButton, QColorDialog, QTabWidget, QFrame, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen, QFont

class CrosshairPreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.crosshair_type = "Cross"
        self.color = QColor("#7F00FF")
        self.thickness = 2
        self.size = 20
        self.opacity = 0.8
        self.setMinimumSize(200, 200)
        self.setMaximumSize(400, 400)

    def set_crosshair_type(self, crosshair_type):
        self.crosshair_type = crosshair_type
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

    def set_thickness(self, thickness):
        self.thickness = thickness
        self.update()

    def set_size(self, size):
        self.size = size
        self.update()

    def set_opacity(self, opacity):
        self.opacity = opacity
        self.update()

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
            # Default to cross
            painter.drawLine(center_x - size, center_y, center_x + size, center_y)
            painter.drawLine(center_x, center_y - size, center_x, center_y + size)

class MainWindow(QMainWindow):
    settings_changed = pyqtSignal()

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("Semente - Crosshair Customizer")
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0F0F0F;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                color: #CCCCCC;
                font-size: 14px;
            }
            QComboBox, QSlider, QPushButton, QLineEdit {
                background-color: #1C1C1C;
                color: white;
                border: 1px solid #7F00FF;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #7F00FF;
                border-radius: 8px;
                width: 16px;
                margin: -4px 0;
            }
            QPushButton:hover {
                background-color: #7F00FF;
                color: black;
            }
        """)

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        main_layout = QHBoxLayout()
        sidebar = QTabWidget()
        sidebar.setStyleSheet("""
            QTabBar::tab {
                background: #1C1C1C;
                color: #CCCCCC;
                padding: 10px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: #7F00FF;
                color: white;
            }
        """)

        # Editor Tab
        editor_tab = QWidget()
        editor_layout = QVBoxLayout()

        # Crosshair Type
        type_label = QLabel("Crosshair Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Point", "Cross", "Circle", "Square"])
        self.type_combo.currentTextChanged.connect(self.on_type_changed)

        # Color Picker
        color_label = QLabel("Color:")
        self.color_button = QPushButton()
        self.color_button.setFixedSize(40, 25)
        self.color_button.clicked.connect(self.open_color_dialog)

        # Thickness Slider
        thickness_label = QLabel("Thickness:")
        self.thickness_slider = QSlider(Qt.Horizontal)
        self.thickness_slider.setMinimum(1)
        self.thickness_slider.setMaximum(10)
        self.thickness_slider.valueChanged.connect(self.on_thickness_changed)

        # Size Slider
        size_label = QLabel("Size:")
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(5)
        self.size_slider.setMaximum(100)
        self.size_slider.valueChanged.connect(self.on_size_changed)

        # Opacity Slider
        opacity_label = QLabel("Opacity:")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(10)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)

        # Hotkey Input
        hotkey_label = QLabel("Toggle Hotkey:")
        self.hotkey_input = QLineEdit()
        self.hotkey_input.setPlaceholderText("Press a key")
        self.hotkey_input.setMaxLength(10)
        self.hotkey_input.textChanged.connect(self.on_hotkey_changed)

        # Animation Test Button
        self.test_animation_button = QPushButton("Test Fade-in Animation")
        self.test_animation_button.clicked.connect(self.test_animation)

        # Preview Widget
        self.preview = CrosshairPreview()

        # Add widgets to layout
        editor_layout.addWidget(type_label)
        editor_layout.addWidget(self.type_combo)
        editor_layout.addWidget(color_label)
        editor_layout.addWidget(self.color_button)
        editor_layout.addWidget(thickness_label)
        editor_layout.addWidget(self.thickness_slider)
        editor_layout.addWidget(size_label)
        editor_layout.addWidget(self.size_slider)
        editor_layout.addWidget(opacity_label)
        editor_layout.addWidget(self.opacity_slider)
        editor_layout.addWidget(hotkey_label)
        editor_layout.addWidget(self.hotkey_input)
        editor_layout.addWidget(self.test_animation_button)
        editor_layout.addStretch()
        editor_layout.addWidget(self.preview, alignment=Qt.AlignCenter)

        editor_tab.setLayout(editor_layout)
        sidebar.addTab(editor_tab, "Editor")

        # Settings Tab (placeholder)
        settings_tab = QWidget()
        settings_layout = QVBoxLayout()
        settings_label = QLabel("Settings will be here.")
        settings_layout.addWidget(settings_label)
        settings_tab.setLayout(settings_layout)
        sidebar.addTab(settings_tab, "Settings")

        # About Tab
        about_tab = QWidget()
        about_layout = QVBoxLayout()
        about_text = QLabel("Semente - Crosshair Overlay App\nVersion 1.0\n© 2024")
        about_text.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(about_text)
        about_tab.setLayout(about_layout)
        sidebar.addTab(about_tab, "About")

        main_layout.addWidget(sidebar)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_settings(self):
        try:
            crosshair = self.config.get_setting("crosshair")
            if crosshair:
                self.type_combo.setCurrentText(crosshair.get("type", "Cross"))
                self.color_button.setStyleSheet(f"background-color: {crosshair.get('color', '#7F00FF')}")
                self.preview.set_color(QColor(crosshair.get("color", "#7F00FF")))
                self.thickness_slider.setValue(crosshair.get("thickness", 2))
                self.size_slider.setValue(crosshair.get("size", 20))
                self.opacity_slider.setValue(int(crosshair.get("opacity", 0.8) * 100))
                self.preview.set_thickness(crosshair.get("thickness", 2))
                self.preview.set_size(crosshair.get("size", 20))
                self.preview.set_opacity(crosshair.get("opacity", 0.8))
            hotkey = self.config.get_setting("hotkey")
            if hotkey:
                self.hotkey_input.setText(hotkey)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load settings: {e}")

    def on_type_changed(self, text):
        self.preview.set_crosshair_type(text)
        self.config.set_setting("crosshair", {**self.config.get_setting("crosshair"), "type": text})
        self.settings_changed.emit()

    def open_color_dialog(self):
        color = QColorDialog.getColor(initial=self.preview.color, parent=self, options=QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self.preview.set_color(color)
            self.color_button.setStyleSheet(f"background-color: {color.name()}")
            self.config.set_setting("crosshair", {**self.config.get_setting("crosshair"), "color": color.name()})
            self.settings_changed.emit()

    def on_thickness_changed(self, value):
        self.preview.set_thickness(value)
        self.config.set_setting("crosshair", {**self.config.get_setting("crosshair"), "thickness": value})
        self.settings_changed.emit()

    def on_size_changed(self, value):
        self.preview.set_size(value)
        self.config.set_setting("crosshair", {**self.config.get_setting("crosshair"), "size": value})
        self.settings_changed.emit()

    def on_opacity_changed(self, value):
        opacity = value / 100.0
        self.preview.set_opacity(opacity)
        self.config.set_setting("crosshair", {**self.config.get_setting("crosshair"), "opacity": opacity})
        self.settings_changed.emit()

    def on_hotkey_changed(self, text):
        self.config.set_setting("hotkey", text)
        self.settings_changed.emit()

    def test_animation(self):
        # Emit signal or call method to trigger fade-in animation on overlay
        QMessageBox.information(self, "Animation", "Fade-in animation test triggered.")
