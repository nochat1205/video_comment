import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QScrollArea, QMessageBox, QSpacerItem, QSizePolicy,
                             QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QColor

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

class ClickableCommentLabel(QLabel):
    clicked = pyqtSignal()  # Define a signal called 'clicked'

    def __init__(self, text='', parent=None):
        super(ClickableCommentLabel, self).__init__(text, parent)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()  # Emit the clicked signal

class ClickableLabel(QLabel):
    # Custom signal that carries the timestamp 't'
    clicked = pyqtSignal()

    def __init__(self, text='', parent=None):
        super(ClickableLabel, self).__init__(text, parent)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

class RowWidget(QWidget):
    timelabel_clicked = pyqtSignal(float)
    comment_clicked = pyqtSignal(float)
    def __init__(self, timestamp, comment, parent=None):
        super().__init__(parent)
        # self.setFrameStyle(QFrame.StyledPanel)  # Optional, adds a visible border
        print("RowWidget:", timestamp)
        self.timestamp = timestamp

        self.layout = QHBoxLayout()
        
        # Setup labels
        timestampLabel = ClickableLabel(f"Timestamp: {format_time(timestamp)}s")
        timestampLabel.clicked.connect(self.on_timestamp_clicked)
        commentLabel = ClickableCommentLabel(comment)
        commentLabel.setWordWrap(True)
        commentLabel.clicked.connect(self.on_comment_clicked)

        # Add to layout
        self.layout.addWidget(timestampLabel)
        self.layout.addWidget(commentLabel)
        self.setLayout(self.layout)

        # Set up for selection
        self.setPalette(QPalette(QColor(240, 240, 240)))
        self.setAutoFillBackground(True)

    def on_comment_clicked(self):
        self.comment_clicked.emit(self.timestamp)

    def on_timestamp_clicked(self):
        print(f"Timestamp {self.timestamp} clicked.")
        self.timelabel_clicked.emit(self.timestamp)

class VideoAnnotationsGUI(QWidget):
    selected_clicked = pyqtSignal(float)
    comment_clicked = pyqtSignal(float)
    def __init__(self, annotations):
        super().__init__()
        self.annotations = annotations
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout()

        # Scroll area setup
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Scrollable container
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        # Initialize comment list
        self.update_comment_list()

        # Delete button
        self.delete_btn = QPushButton('Delete Comment', self)
        self.delete_btn.clicked.connect(self.delete_comment)
        layout.addWidget(self.delete_btn)

        # Set the main layout
        self.setLayout(layout)
        self.setGeometry(300, 300, 350, 400)
        self.setWindowTitle('Video Annotations')

    def update_comment_list(self):
        """Update the QWidget inside the QScrollArea with current comments."""
        # Remember the current scroll position
        scroll_bar = self.scroll_area.verticalScrollBar()
        was_at_bottom = scroll_bar.value() == scroll_bar.maximum()

        # Clear current widgets in the layout
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add new labels for each comment
        for comment in self.annotations.get_comments():
            print("update_comment_list:", comment)
            row_widget = RowWidget(comment['t'], comment['comment'], self.scroll_widget)

            row_widget.timelabel_clicked.connect(self.timestamp_clicked)  # You would need to add a signal for clicks
            row_widget.comment_clicked.connect(self.row_clicked)
            self.scroll_layout.addWidget(row_widget)

        # Add a spacer to push all content up
        self.scroll_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Restore scroll position
        if was_at_bottom:
            scroll_bar.setValue(scroll_bar.maximum())

    def row_selected(self, row_widget):
        if self.selected_row:
            self.selected_row.setPalette(QPalette(QColor(240, 240, 240)))  # Reset previous selection color
        self.selected_row = row_widget
        self.selected_row.setPalette(QPalette(QColor(200, 200, 255)))  # Highlight selected row

    def delete_comment(self):
        """Delete the selected comment."""
        if self.annotations.del_comment(self.selected_timestamp):
            self.update_comment_list()
        else:
            QMessageBox.warning(self, 'Deletion Error', 'No comments to delete.')

        self._add_operator()

    def timestamp_clicked(self, timestamp):
        print(f"Timestamp {timestamp} clicked!")
        self.selected_clicked.emit(timestamp)

    def row_clicked(self, timestamp):
        self.selected_timestamp = timestamp

def main():
    from VideoAnnotations import VideoAnnotations
    app = QApplication(sys.argv)
    annotations = VideoAnnotations()
    ex = VideoAnnotationsGUI(annotations)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
