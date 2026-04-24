"""Main application window with home screen and mode navigation."""
import tkinter as tk
from game.scoring import ScoreManager
from game.mode_draw import DrawMode
from game.mode_guess import GuessMode

BG = "#F0F4F8"
ACCENT = "#4A90D9"
DARK = "#2C3E50"


class App:
    TITLE = "你画我猜 - Draw & Guess"
    WIDTH = 720
    HEIGHT = 650

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(self.TITLE)
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.score_mgr = ScoreManager()
        self.current_frame = None

        self._show_home()

    def _clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None

    def _show_home(self):
        self._clear_frame()
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True, fill="both")
        self.current_frame = frame

        # Title area
        title_frame = tk.Frame(frame, bg=BG)
        title_frame.pack(pady=(50, 10))
        tk.Label(title_frame, text="你画我猜", font=("Microsoft YaHei", 40, "bold"),
                 bg=BG, fg=DARK).pack()
        tk.Label(title_frame, text="Draw & Guess", font=("Arial", 16),
                 bg=BG, fg="#7F8C8D").pack(pady=5)

        # Score display
        if self.score_mgr.total:
            tk.Label(frame, text=f"当前得分: {self.score_mgr.total}",
                     font=("Microsoft YaHei", 15), bg=BG, fg=ACCENT).pack(pady=15)

        # Mode buttons
        btn_frame = tk.Frame(frame, bg=BG)
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="我画电脑猜", font=("Microsoft YaHei", 18, "bold"),
                  width=16, height=2, bg=ACCENT, fg="white", relief="flat",
                  activebackground="#357ABD", activeforeground="white",
                  command=self._start_draw_mode).pack(pady=12)
        tk.Button(btn_frame, text="电脑画我猜", font=("Microsoft YaHei", 18, "bold"),
                  width=16, height=2, bg="#27AE60", fg="white", relief="flat",
                  activebackground="#219A52", activeforeground="white",
                  command=self._start_guess_mode).pack(pady=12)

        # Reset button
        if self.score_mgr.total:
            tk.Button(frame, text="重置分数", font=("Microsoft YaHei", 10),
                      bg="#95A5A6", fg="white", relief="flat", padx=10,
                      command=self._reset_score).pack(pady=20)

        # Footer
        tk.Label(frame, text="限时30秒 | 猜对得分 | 连续答对有额外奖励",
                 font=("Microsoft YaHei", 10), bg=BG, fg="#95A5A6").pack(side="bottom", pady=15)

    def _start_draw_mode(self):
        self._clear_frame()
        frame = DrawMode(self.root, self.score_mgr, on_back=self._show_home)
        frame.pack(expand=True, fill="both")
        self.current_frame = frame

    def _start_guess_mode(self):
        self._clear_frame()
        frame = GuessMode(self.root, self.score_mgr, on_back=self._show_home)
        frame.pack(expand=True, fill="both")
        self.current_frame = frame

    def _reset_score(self):
        self.score_mgr.reset()
        self._show_home()

    def run(self):
        self.root.mainloop()
