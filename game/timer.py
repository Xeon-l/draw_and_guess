"""30-second countdown timer using Tkinter after()."""


class CountdownTimer:
    def __init__(self, root, label, on_timeout=None, seconds=30):
        self.root = root
        self.label = label
        self.on_timeout = on_timeout
        self.total_seconds = seconds
        self.remaining = seconds
        self._job = None
        self.running = False

    def start(self):
        self.remaining = self.total_seconds
        self.running = True
        self._update_display()
        self._tick()

    def stop(self):
        self.running = False
        if self._job:
            self.root.after_cancel(self._job)
            self._job = None

    def _tick(self):
        if not self.running:
            return
        if self.remaining <= 0:
            self.running = False
            self.label.config(text="时间到!")
            if self.on_timeout:
                self.on_timeout()
            return
        self._update_display()
        self.remaining -= 1
        self._job = self.root.after(1000, self._tick)

    def _update_display(self):
        self.label.config(text=f"⏱ {self.remaining}s")
