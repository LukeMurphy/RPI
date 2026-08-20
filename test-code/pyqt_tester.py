import sys, time
from PIL import Image, ImageDraw, ImageFilter
from PyQt6.QtCore import QSize, Qt, QThread, QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget
from PIL.ImageQt import ImageQt
from PyQt6 import QtCore, QtGui, QtWidgets

# Subclass QMainWindow to customize your application's main window


class Worker(QObject):
    finished = pyqtSignal()

    def setup(self, parent):
        self.window = parent

    def run(self):
        time.sleep(0.02)
        self.window.updateAnimation()
        self.run()
        # Simulate a long-running task
        # self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)
        self.setFixedSize(QSize(400, 300))

        widget = QListWidget()
        widget.addItems(["One", "Two", "Three"])

        widget.currentItemChanged.connect(self.index_changed)
        widget.currentTextChanged.connect(self.text_changed)

        # self.setCentralWidget(widget)

        self.canvas = Image.new("RGBA", (200, 200))
        self.canvasDraw = ImageDraw.Draw(self.canvas)
        self.canvasDraw.rectangle((10, 10, 120, 140), fill=(255, 0, 0, 175), outline=(0, 255, 0, 175))

        self.xPos = 0
        self.yPos = 0

        self.canvasObj = QtWidgets.QLabel()

        self.im = ImageQt(self.canvas)
        self.pixmap = QtGui.QPixmap.fromImage(self.im)
        self.canvasObj.setPixmap(self.pixmap)
        self.setCentralWidget(self.canvasObj)

        # self.start_task()

    def start_task(self):
        self.label = QtWidgets.QLabel()
        self.label.setText("Task running...")
        self.thread = QThread()
        self.worker = Worker()
        self.worker.setup(self)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self):
        self.label.setText("Task completed!")
        self.thread.quit()
        self.thread.wait()
        exit()

    def index_changed(self, i):  # Not an index, i is a QListWidgetItem
        print(i.text())

    def text_changed(self, s):  # s is a str
        print(s)

    def updateAnimation(self):
        self.xPos += 1

        if self.xPos > 200 :
            self.xPos = -200
        self.canvasDraw.rectangle((0, 0, 200, 200), fill=(0, 0, 0, 0))
        self.canvasDraw.rectangle((10 + self.xPos, 10, 120 + self.xPos, 140), fill=(255, 0, 0, 175), outline=(0, 255, 0, 175))

        self.im = ImageQt(self.canvas)
        self.pixmap = QtGui.QPixmap.fromImage(self.im)
        self.canvasObj.setPixmap(self.pixmap)
        QApplication.processEvents()
        # self.setCentralWidget(self.canvasObj)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.start_task()
sys.exit(app.exec())
