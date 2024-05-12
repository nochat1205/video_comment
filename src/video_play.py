import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from .widgets.ClickableProgressBar import ClickableProgressBar
from .widgets.InputComment import CommentUI

def adjust_size(parent_width, parent_height, video_width, video_height):
    # Calculate scaling factors
    width_ratio = parent_width / video_width
    height_ratio = parent_height / video_height

    # Choose the smaller scaling factor to ensure the entire video fits within the parent widget
    scale_factor = min(width_ratio, height_ratio)

    # Calculate the new width and height
    new_width = int(video_width * scale_factor)
    new_height = int(video_height * scale_factor)

    return new_width, new_height


class VideoPlayer(QWidget):
    comment = pyqtSignal(float, str)

    # Vlayout: {self.label(image), button}
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MoviePy Video Player')
        self.setGeometry(100, 100, 800, 600)

        self.clip = None

        # Player controls
        self.playButton = QPushButton('Play')
        self.playButton.clicked.connect(self.toggle_playback)
        self.is_playing = False

        self.slowButton = QPushButton('Slow')
        self.slowButton.clicked.connect(self.slow_playback)

        self.fastButton = QPushButton('Fast')
        self.fastButton.clicked.connect(self.fast_playback)

        self.progressSlider = ClickableProgressBar()
        self.progressSlider.valueChanged.connect(self.slider_moved)

        self.timeLabel = QLabel("00:00 / 00:00")  # Time display label
        self.timeLabel.setAlignment(Qt.AlignCenter)

        # Layouts
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.playButton)
        control_layout.addWidget(self.slowButton)
        control_layout.addWidget(self.fastButton)
        control_layout.addWidget(self.progressSlider)
        control_layout.addWidget(self.timeLabel)  # Add the time label to the layout


        # comment
        commentUI = CommentUI()
        commentUI.comment.connect(self.on_comment)

        main_layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setScaledContents(True)
        main_layout.addWidget(self.label)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(commentUI)

        self.setLayout(main_layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def open_file(self, file):
        # Load video using MoviePy
        self.clip = VideoFileClip(file)
        self.total_duration = self.clip.duration  # Total duration in seconds
        self.frame_rate = self.clip.fps  # Frames per second
        self.current_time = 0
        self.total_frames = int(self.frame_rate * self.total_duration)

        self.normal_speed = int(self.total_frames / self.frame_rate)
        self.timer.setInterval(self.normal_speed)
        self.progressSlider.setMaximum(self.total_frames)
        self.update_frame()

    def toggle_playback(self):
        if self.clip is None:
            return

        if self.is_playing:
            self.timer.stop()
            self.playButton.setText('Play')
        else:
            self.timer.start(self.normal_speed)
            self.playButton.setText('Pause')
        self.is_playing = not self.is_playing

    def slow_playback(self):
        if self.is_playing:
            self.timer.setInterval(int(self.normal_speed * 2))  # Slower playback

    def fast_playback(self):
        if self.is_playing:
            self.timer.setInterval(int(self.normal_speed / 2))  # Faster playback

    def update_frame(self):
        self.set_frame(self.current_time + 1 / self.frame_rate)

    def slider_moved(self):
        self.set_frame(self.progressSlider.value() / self.total_frames * self.total_duration)

    def set_frame(self, t):
        if t >= self.total_duration:
            self.timer.stop()
            self.playButton.setText('Play')
            self.is_playing = False
            t = 0
        self.current_time = t
        print("set_frame self.current_time:", t)
        frame = self.clip.get_frame(t)
        qimg = QImage(frame.tobytes(), frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qimg)

        # new_width, new_height = adjust_size(self.size().width(), self.size().height(), frame.shape[0], frame.shape[1])
        # self.label.resize(new_width, new_height)

        scaled_pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 根据label大小调整pixmap大小，保持横纵比
        self.label.setPixmap(scaled_pixmap)
        value = t / self.total_duration * self.total_frames
        self.progressSlider.setValue(value)

        # Update the time display
        current_time_str = self.format_time(self.current_time)
        total_time_str = self.format_time(self.total_duration)
        self.timeLabel.setText(f"{current_time_str} / {total_time_str}")

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    def on_comment(self, comment):
        print("on_comment self.current_time:", self.current_time)
        self.comment.emit(self.current_time, comment)

if __name__ == '__main__':
    # import os
    # import sys
    # sys.path.append(os.getcwd())
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    player.open_file(r'.\source\3343679-hd_1920_1080_30fps.mp4')
    sys.exit(app.exec_())
