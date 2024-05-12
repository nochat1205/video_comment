
from PyQt5.QtWidgets import QApplication
from src.video_mark import MainWindow
import sys

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    player = MainWindow()
    player.show()
    sys.exit(app.exec_())
