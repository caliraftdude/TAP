"""
Class Robot


"""
import time
from .actor import Actor
from .script import Script


# Robots are actors which accept commands to perform actions.
# They can also record and run scripts.
class Robot(Actor):
    def __init__(self, name):
        Robot.__init__(self, name)
        self.name = name
        self.scripts = {}
        self.current_script = None
        self.script_think_time = 0
        self.verbs["record"] = self.act_start_recording
        self.verbs["run"] = self.act_run_script
        self.verbs["print"] = self.act_print_script
        self.verbs["save"] = self.act_save_file
        self.verbs["load"] = self.act_load_file
        self.verbs["think"] = self.set_think_time

    def __repr__(self)->str:
        return "<Class 'Robot'>"

    def __str__(self) -> str:
        return f"Todo"

    def parse_script_name(self, words):
        if not words or len(words) < 2:
            script_name = "default"
        else:
            script_name = words[1]
        return script_name

    def act_start_recording(self, actor, words=None):
        script_name = self.parse_script_name(words)
        script = Script(script_name)
        self.scripts[script_name] = script
        script.start_recording()
        self.current_script = script
        return True

    def act_run_script(self, actor, words=None):
        if self.current_script:
            print('You must stop "%s" first.' % (self.current_script.name))
        script_name = self.parse_script_name(words)
        if not script_name in self.scripts:
            print(
                '%s can\'t find script "%s" in its memory.' % (self.name, script_name)
            )

            return True

        script = self.scripts[script_name]
        self.current_script = script
        script.start_running()
        return True

    def act_print_script(self, actor, words=None):
        script_name = self.parse_script_name(words)
        if not script_name in self.scripts:
            print(
                '%s can\'t find script "%s" in its memory.' % (self.name, script_name)
            )
            return True

        print("----------------------8<-------------------------")
        self.scripts[script_name].print_lines()
        print("---------------------->8-------------------------")
        return True

    def act_save_file(self, actor, words=None):
        script_name = self.parse_script_name(words)
        if not script_name in self.scripts:
            print(
                '%s can\'t find script "%s" in its memory.' % (self.name, script_name)
            )
            return True
        self.scripts[script_name].save_file()
        return True

    def act_load_file(self, actor, words=None):
        script_name = self.parse_script_name(words)
        self.scripts[script_name] = Script(script_name)
        self.scripts[script_name].load_file()
        return True

    def set_think_time(self, actor, words):
        if words and len(words) == 2:
            t = float(words[1])
            if t >= 0 and t <= 60:
                self.script_think_time = t
                return True

        print('"think" requires a number of seconds (0-60) as an argument')
        return True

    def get_next_script_line(self):
        if not self.current_script or not self.current_script.running:
            return None
        line = self.current_script.get_next_line()
        if not line:
            print(
                '%s is done running script "%s".'
                % (self.name, self.current_script.name)
            )
            self.current_script = None
            return None
        if self.script_think_time > 0:
            time.sleep(self.script_think_time)
        line = self.name + ": " + line
        print("> %s" % line)
        return line

    def set_next_script_line(self, line):
        if not self.current_script or not self.current_script.recording:
            return True
        if not self.current_script.set_next_line(line):
            print(
                '%s finished recording script "%s".'
                % (self.name, self.current_script.name)
            )
            self.current_script = None
            return False
        return True