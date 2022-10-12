"""
Class Scripts

Scripts are sequences of instructions for Robots to execute.  The script class allows you to
start and stop recording, playback, etc... as well as save and load the script from file.

XXX Instead of a file, it would be better if a resource system was implemented that could
retrieve a script.

"""
from .base import Base


class Script(Base):
    def __init__(self, name):
        Base.__init__(self, name)
        self.lines = list()
        self.current_line = -1
        self.recording = False
        self.running = False

    def __repr__(self)->str:
        return "<Class 'Script'>"

    def __str__(self) -> str:
        return f"Lines ({len(self.lines)}):\n{self.lines}\nCurrent Line: {self.current_line}\nRecording: {self.recording}\nRunning: {self.running}"

    def start_recording(self):
        assert not self.running
        assert not self.recording
        self.recording = True

    def stop_recording(self):
        assert self.recording
        assert not self.running
        self.recording = False

    def start_running(self):
        assert not self.running
        assert not self.recording
        self.running = True
        self.current_line = 0

    def stop_running(self):
        assert self.running
        assert not self.recording
        self.running = False
        self.current_line = -1

    def get_next_line(self):
        line = self.lines[self.current_line]
        self.current_line += 1
        if line.strip() == "end":
            self.stop_running()
            return None
        return line

    def set_next_line(self, line):
        self.lines.append(line)
        if line.strip() == "end":
            self.stop_recording()
            return False
        return True

    def print_lines(self):
        for line in self.lines:
            print(line)

    def save_file(self):
        f = open(self.name + ".script", "w")
        for line in self.lines:
            f.write(line + "\n")
        f.close()

    def load_file(self):
        f = open(self.name + ".script", "r")
        for line in f:
            self.lines.append(line.strip())
        f.close()