"""我画电脑猜 mode: player draws, AI guesses."""
import tkinter as tk
import random
from game.canvas import DrawingCanvas
from game.timer import CountdownTimer
from game.words import get_random_word, get_hint, ALL_WORDS

BG = "#F0F4F8"
ACCENT = "#4A90D9"
GREEN = "#27AE60"
RED = "#E74C3C"
DARK = "#2C3E50"


class DrawMode(tk.Frame):
    def __init__(self, master, score_mgr, on_back=None, **kwargs):
        super().__init__(master, bg=BG, **kwargs)
        self.score_mgr = score_mgr
        self.on_back = on_back
        self.word_entry = None
        self.guess_attempts = 0
        self.max_guesses = 3

        self._build_ui()
        self._new_round()

    def _build_ui(self):
        # Top bar
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=15, pady=8)
        tk.Button(top, text="返回首页", font=("Microsoft YaHei", 10),
                  bg="#95A5A6", fg="white", relief="flat", padx=10,
                  command=self._go_back).pack(side="left")
        self.score_label = tk.Label(top, text=f"得分: {self.score_mgr.total}",
                                    font=("Microsoft YaHei", 13, "bold"), bg=BG, fg=DARK)
        self.score_label.pack(side="right")

        # Word + Timer row
        info = tk.Frame(self, bg=BG)
        info.pack(fill="x", padx=15)
        self.word_label = tk.Label(info, text="", font=("Microsoft YaHei", 22, "bold"), bg=BG, fg=ACCENT)
        self.word_label.pack(side="left")
        self.timer_label = tk.Label(info, text="", font=("Microsoft YaHei", 14, "bold"), bg=BG, fg=RED)
        self.timer_label.pack(side="right")

        # Canvas (smaller to leave room for controls)
        self.canvas_widget = DrawingCanvas(self, width=480, height=280)
        self.canvas_widget.pack(padx=15, pady=5)

        # Action bar: hint left, submit right
        action = tk.Frame(self, bg=BG)
        action.pack(fill="x", padx=15, pady=5)
        tk.Button(action, text="提示", font=("Microsoft YaHei", 11),
                  bg="#F39C12", fg="white", relief="flat", padx=12,
                  command=self._show_hint).pack(side="left")
        tk.Button(action, text="提交给电脑猜", font=("Microsoft YaHei", 11, "bold"),
                  bg=ACCENT, fg="white", relief="flat", padx=16,
                  command=self._submit).pack(side="right")

        # Hint label
        self.hint_label = tk.Label(self, text="", font=("Microsoft YaHei", 11), bg=BG, fg="#7F8C8D")
        self.hint_label.pack(padx=15)

        # Result area (below hint)
        self.result_frame = tk.Frame(self, bg=BG)

        self.timer = CountdownTimer(self.winfo_toplevel(), self.timer_label, on_timeout=self._on_timeout)

    def _new_round(self):
        self.result_frame.pack_forget()
        self.word_entry = get_random_word()
        self.word_label.config(text=f"请画: {self.word_entry['word']}")
        self.hint_label.config(text="")
        self.guess_attempts = 0
        self.canvas_widget.clear()
        self.timer.start()
        self.score_label.config(text=f"得分: {self.score_mgr.total}")

    def _show_hint(self):
        hint = get_hint(self.word_entry)
        self.hint_label.config(text=hint)

    def _submit(self):
        self.timer.stop()
        self.guess_attempts += 1
        all_words = [w["word"] for w in ALL_WORDS]

        if self.guess_attempts >= self.max_guesses:
            ai_guess = self.word_entry["word"]
        else:
            ai_guess = random.choice([w for w in all_words if w != self.word_entry["word"]])

        self._show_guess_result(ai_guess)

    def _show_guess_result(self, ai_guess):
        self.result_frame.destroy()
        self.result_frame = tk.Frame(self, bg=BG)
        self.result_frame.pack(pady=5)

        tk.Label(self.result_frame, text=f"电脑猜的是: {ai_guess}",
                 font=("Microsoft YaHei", 15), bg=BG, fg=DARK).pack()

        if ai_guess == self.word_entry["word"]:
            earned = self.score_mgr.add_correct(self.timer.remaining)
            tk.Label(self.result_frame, text=f"电脑猜对了!  +{earned}分",
                     font=("Microsoft YaHei", 13, "bold"), bg=BG, fg=GREEN).pack(pady=3)
        else:
            self.score_mgr.add_wrong()
            tk.Label(self.result_frame, text="电脑猜错了!",
                     font=("Microsoft YaHei", 13), bg=BG, fg=RED).pack(pady=3)

        btn_row = tk.Frame(self.result_frame, bg=BG)
        btn_row.pack(pady=5)
        tk.Button(btn_row, text="下一题", font=("Microsoft YaHei", 11),
                  bg=ACCENT, fg="white", relief="flat", padx=12,
                  command=self._new_round).pack(side="left", padx=8)
        tk.Button(btn_row, text="其实猜对了", font=("Microsoft YaHei", 11),
                  bg=GREEN, fg="white", relief="flat", padx=12,
                  command=self._force_correct).pack(side="left", padx=8)

        self.score_label.config(text=f"得分: {self.score_mgr.total}")

    def _force_correct(self):
        if self.word_entry:
            self.score_mgr.add_correct(self.timer.remaining)
            self.score_label.config(text=f"得分: {self.score_mgr.total}")
        self._new_round()

    def _on_timeout(self):
        self.score_mgr.add_wrong()
        self.result_frame.destroy()
        self.result_frame = tk.Frame(self, bg=BG)
        self.result_frame.pack(pady=5)
        tk.Label(self.result_frame, text="时间到!", font=("Microsoft YaHei", 15, "bold"), bg=BG, fg=RED).pack()
        tk.Label(self.result_frame, text=f"答案: {self.word_entry['word']}",
                 font=("Microsoft YaHei", 13), bg=BG, fg=DARK).pack(pady=3)
        tk.Button(self.result_frame, text="下一题", font=("Microsoft YaHei", 11),
                  bg=ACCENT, fg="white", relief="flat", padx=12,
                  command=self._new_round).pack(pady=5)
        self.score_label.config(text=f"得分: {self.score_mgr.total}")

    def _go_back(self):
        self.timer.stop()
        if self.on_back:
            self.on_back()
