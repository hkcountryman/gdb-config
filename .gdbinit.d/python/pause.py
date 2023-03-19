class DynamicExpressions(Expressions):
    """Watch variables dynamically."""

    stopped = True

    def __init__(self):
        super().__init__()
        #gdb.events.stop.connect(do)

    def label(self):
        return "Dynamic Expressions"

    def commands(self):
        cmds = super().commands()
        return {
            **cmds,
            "go": {
                "action": self.go,
                "doc": "Continue execution."
            },
            "stop": {
                "action": self.stop,
                "doc": "Stop execution (manual break)."
            },
            "beep": {
                "action": self.beep,
                "doc": "Log a beep."
            }
        }

    def beep(self, arg):
        gdb.post_event(Beeper())

    def go(self, arg):
        gdb.post_event(Goer())

    def stop(self, arg):
        gdb.post_event(Stopper())

    def do(event):
        if not stopped:
            gdb.execute("set scheduler-locking on") # to avoid parallel signals in other threads
            gdb.write(event.stop_signal)
            frame = gdb.selected_frame()
            while frame:
                frame = frame.older()
            gdb.execute("set scheduler-locking off") # otherwise just this thread is continued, leading to a deadlock
        else:
            gdb.post_event(Goer())


class Goer():
    def __call__(self):
        gdb.execute("continue")


class Stopper():
    def __call__(self):
            gdb.execute("set scheduler-locking on") # to avoid parallel signals in other threads
            gdb.execute("signal stop")
            frame = gdb.selected_frame()
            while frame:
                frame = frame.older()
            gdb.execute("set scheduler-locking off") # otherwise just this thread is continued, leading to a deadlock

