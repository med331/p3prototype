import time


class Logger:

    def __init__(self):
        self.time_stamp = 0
        self.frames_this_second = 0
        self.lines = []

    def new_frame(self):
        if time.time() - self.time_stamp >= 1:
            self.lines.append(str(self.frames_this_second))
            self.log_data()
            self.frames_this_second = 0
            self.time_stamp = time.time()
        else:
            self.frames_this_second = self.frames_this_second + 1

    def log_data(self):
        with open("stats.txt", 'w') as file:
            final_string = ""
            for line in self.lines:
                final_string += ", %s" % line
            file.write(final_string[5:])