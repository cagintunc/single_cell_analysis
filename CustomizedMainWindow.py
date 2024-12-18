from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5 import QtWidgets

class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drag_start = None
        self.init_ui()

    def init_ui(self):
        # Remove the default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(800, 600)  # Set initial size
        self.center_window()   # Center the window

        # Create a central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Add a vertical layout
        layout = QVBoxLayout(self.central_widget)

        # Create a custom title bar
        self.title_bar = QWidget(self)
        self.title_bar.setStyleSheet("background-color: #2c3e50; color: white;")
        self.title_bar.setFixedHeight(40)

        # Add a layout to the title bar
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Add a spacer to push the close button to the right
        spacer = QWidget(self.title_bar)
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        title_layout.addWidget(spacer)

        # Add a close button to the title bar
        close_button = QPushButton("X", self.title_bar)
        close_button.setFixedSize(30, 30)  # Small button size
        close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff4d4d; /* Lighter red on hover */
            }
        """)
        close_button.clicked.connect(self.close)
        title_layout.addWidget(close_button)

        # Add the title bar and the main content to the layout
        layout.addWidget(self.title_bar)
        layout.addWidget(QLabel("Main Application Content"))

    def center_window(self):
        # Get the screen's geometry
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Calculate the center point
        center_point = screen_geometry.center()

        # Move the window to the center
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    # Override mousePressEvent for dragging the window
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start)
            event.accept()

