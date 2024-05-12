import json

class VideoAnnotations:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self._init_data()
        if file_path:
            self.load(file_path)

        self.save_operator = -1
        self.operator_count = 0

    def _init_data(self):
        self.file_path = None
        self.data = {
            "video_path": "",
            "t": 0,
            "comments": []
        }

    def set_video_path(self, path):
        """Set the path of the video."""
        if self.IsSaved() or len(self.data['video_path']) == 0:
            self.data['video_path'] = path
            return True
        else:
            return False

    def get_video_path(self):
        return self.data['video_path']

    def load(self, file_path):
        """Load annotations from a JSON file."""
        self._init_data()
        try:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
                self.file_path = file_path
                self.operator_count = 0
                self.save_operator = self.operator_count

        except FileNotFoundError:
            print("File not found. Starting with an empty annotations set.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Starting with an empty annotations set.")
        return True

    def _add_operator(self):
        self.operator_count += 1
        if self.operator_count % 1 == 0:
            self.save()

    def IsSaved(self):
        return self.file_path and self.save_operator == self.operator_count

    def new(self):
        if self.IsSaved():
            self._init_data()
            return True
        else:
            return False

    def save(self):
        """Save the current annotations back to the file."""
        if self.file_path:
            with open(self.file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
            self.save_operator = self.operator_count
            return True
        else:
            print("File path is not set. Use 'save_as' to specify a file path.")
            return False

    def get_file_path(self):
        return self.file_path

    def save_as(self, file_path):
        """Save the current annotations to a new file."""
        self.file_path = file_path
        self.save()

    def add_comment(self, timestamp, comment):
        """Add a new comment to the annotations."""
        print("add_comment: timestamp :", timestamp)
        self.data['comments'].append({"t": timestamp, "comment": comment})
        self._add_operator()

    def del_comment(self, timestamp):
        comments = self.annotations.data['comments']
        if self.annotations.data['comments']:
            for ind, comment in enumerate(comments):
                if comment['t'] == timestamp:
                    del self.annotations.data['comments'][ind]

            return True
        else:
            return False

    def set_initial_timestamp(self, timestamp):
        """Set the initial timestamp."""
        self.data['t'] = timestamp

    def get_comments(self):
        """Get all comments."""
        return self.data['comments']

    def __str__(self):
        return json.dumps(self.data, indent=4)

