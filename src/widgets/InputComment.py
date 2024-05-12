import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QLineEdit, QPushButton,
)
from PyQt5.QtCore import Qt, QEvent, pyqtSignal

class CommentUI(QWidget):
    comment = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Horizontal layout
        h_layout = QHBoxLayout()
        
        # Create a QLineEdit for input
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter your comment here...")
        
        # Create a QPushButton for submitting the comment
        self.comment_button = QPushButton("Comment", self)
        self.comment_button.clicked.connect(self.on_click)
        
        # Add widgets to the layout
        h_layout.addWidget(self.input_field)
        h_layout.addWidget(self.comment_button)
        
        # Set the layout to the QWidget
        self.setLayout(h_layout)
        self.setGeometry(300, 300, 400, 50)  # Set the size and position of the window
        self.setWindowTitle('PyQt5 Input and Button')  # Set the window title

    def on_click(self):
        # Function to handle button click
        # This could be expanded to actually do something with the input, like storing it or displaying it
        comment = self.input_field.text()
        # print("Comment entered:", comment)  # For now, just print it to the console
        self.comment.emit(comment)

def main():
    app = QApplication(sys.argv)
    ex = CommentUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
