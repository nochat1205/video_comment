
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QEvent, pyqtSignal

from .video_play import VideoPlayer
from .CommentsWindow import VideoAnnotationsGUI
from .VideoAnnotations import VideoAnnotations

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QFileDialog, QDockWidget
from PyQt5.QtCore import Qt
# Assuming VideoPlayer and VideoAnnotations, VideoAnnotationsGUI are already defined

class MainWindow(QMainWindow):
    last_work_annotation = "./temp/annotation.json"
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_annotations(MainWindow.last_work_annotation)

    def initUI(self):
        self.setWindowTitle('Video and Comments Application')
        self.setGeometry(100, 100, 800, 600)

        # Menu bar setup
        self.setup_menus()

        # Video playback widget
        self.video_player = VideoPlayer()
        self.setCentralWidget(self.video_player)

        # Comments dock widget
        self.annotations = VideoAnnotations()
        self.comments_widget = VideoAnnotationsGUI(self.annotations)
        dock_widget = QDockWidget("Comments", self)
        dock_widget.setWidget(self.comments_widget)


        # Setting the initial size of the comments widget
        self.comments_widget.setFixedSize(300, 600)  # For example, 200px width and 600px height
        # Optionally, set the minimum and maximum size of the dock widget if needed
        dock_widget.setMinimumSize(300, 600)  # Minimum size
        dock_widget.setMaximumSize(400, 1000)  # Maximum size
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        # Load a video file
        # self.video_player.open_file(r'.\source\3343679-hd_1920_1080_30fps.mp4')

        # event
        self.video_player.comment.connect(self.on_update_annotations)
        self.comments_widget.selected_clicked.connect(self.on_select_frame)

    def on_select_frame(self, t):
        self.video_player.set_frame(t)

    def on_update_annotations(self, t, comment):
        self.annotations.add_comment(t, comment)
        self.comments_widget.update_comment_list()

    def setup_menus(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu('File')

        # Load video action
        load_video_action = QAction('Load Video', self)
        load_video_action.triggered.connect(self.load_video)
        file_menu.addAction(load_video_action)

        # Save As action
        save_as_action = QAction('Save As...', self)
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)

        # Annotations menu
        annotations_menu = menu_bar.addMenu('Annotations')

        # Read annotations action
        read_annotations_action = QAction('Read Annotations', self)
        read_annotations_action.triggered.connect(self.read_annotations)
        annotations_menu.addAction(read_annotations_action)

        # Save annotations action
        save_annotations_action = QAction('Save Annotations', self)
        save_annotations_action.triggered.connect(self.save_annotations)
        annotations_menu.addAction(save_annotations_action)

        # New annotations action
        new_annotations_action = QAction('New Annotations', self)
        new_annotations_action.triggered.connect(self.new_annotations)
        annotations_menu.addAction(new_annotations_action)

    def load_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if file_name:
            if self.annotations.set_video_path(file_name):
                self.video_player.open_file(file_name)
            else:
                QMessageBox.warning(self, 'set video failed', 'set video failed.')

    def save_as(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Video As", "", "Video Files (*.mp4 *.avi *.mov)")
        if file_name:
            # Implement logic to save the video file as a new file
            self.annotations.save_as(file_name)

    def read_annotations(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Annotation File", "", "Annotation Files (*.json *.txt)")
        self.load_annotations(file_name)

    def load_annotations(self, file_name):
        if file_name:
            self.annotations.load(file_name)
            self.comments_widget.update_comment_list()
            print(self.annotations.get_video_path())
            self.video_player.open_file(self.annotations.get_video_path())

    def save_annotations(self):
        if self.annotations.get_file_path():
            self.annotations.save()
            return True

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Annotations", "", "Annotation Files (*.json *.txt)")
        if file_name:
            self.annotations.save_as(file_name)

    def new_annotations(self):
        self.annotations.new()

    def closeEvent(self, event):
        if not self.annotations.IsSaved():
            reply = QMessageBox.question(self, 'Unsaved Changes',
                                         "You have unsaved changes. Do you want to save them before exiting?",
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                         QMessageBox.Save)

            if reply == QMessageBox.Save:
                self.save_annotations()  # Assuming save_annotations method handles saving
                event.accept()  # Proceed with the closure
            elif reply == QMessageBox.Discard:
                event.accept()  # Ignore the changes and proceed with the closure
            else:
                event.ignore()  # Cancel the closure
        else:
            event.accept()  # Proceed with the closure if no changes need saving

        self.annotations.save_as(MainWindow.last_work_annotation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
