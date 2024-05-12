from PyQt5.QtWidgets import QApplication, QSlider, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent, pyqtSignal

class ClickableProgressBar(QWidget):
    valueChanged = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMaximum(1000)  # 设置进度条范围
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)

        layout = QVBoxLayout(self)
        layout.addWidget(self.slider)

        self.setLayout(layout)
        self.setWindowTitle('Clickable Progress Bar Example')
        self.setGeometry(300, 300, 280, 170)

        # 连接信号
        # self.slider.valueChanged.connect(self.emitValueChanged)
        self.slider.installEventFilter(self)  # 安装事件过滤器

    def setMaximum(self, value):
        self.slider.setMaximum(value)

    def eventFilter(self, obj, event):
        if obj is self.slider and event.type() == QEvent.MouseButtonRelease:
            # 计算点击位置对应的滑块值
            val = self.slider.minimum() + ((self.slider.maximum() - self.slider.minimum()) * event.x()) / self.slider.width()
            print("self.slider.setValue:", val)
            self.slider.setValue(int(val))
            self.valueChanged.emit(val)
            return True
        return super().eventFilter(obj, event)

    def setValue(self, value):
        self.slider.setValue(int(value))

    def value(self):
        return self.slider.value()

if __name__ == "__main__":
    app = QApplication([])
    ex = ClickableProgressBar()
    ex.show()
    app.exec_()
