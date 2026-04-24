"""电脑画我猜 mode: AI draws, player guesses."""
import tkinter as tk
import os
import random
from PIL import Image, ImageTk
from game.timer import CountdownTimer
from game.words import get_hint, ALL_WORDS
from game.sketch_fetcher import get_sketch_path, get_all_sketchable_words, prefetch_words

BG = "#F0F4F8"
ACCENT = "#4A90D9"
GREEN = "#27AE60"
RED = "#E74C3C"
DARK = "#2C3E50"


class GuessMode(tk.Frame):
    def __init__(self, master, score_mgr, on_back=None, **kwargs):
        super().__init__(master, bg=BG, **kwargs)
        self.score_mgr = score_mgr
        self.on_back = on_back
        self.current_word = None
        self.current_word_entry = None
        self.sketch_photo = None

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

        # Timer
        self.timer_label = tk.Label(self, text="", font=("Microsoft YaHei", 14, "bold"), bg=BG, fg=RED)
        self.timer_label.pack(pady=3)

        # Sketch display area — fixed pixel size via Canvas
        canvas_frame = tk.Frame(self, bg="white", relief="groove", bd=2)
        canvas_frame.pack(padx=15, pady=8)
        self.sketch_canvas = tk.Canvas(canvas_frame, width=420, height=300, bg="white", highlightthickness=0)
        self.sketch_canvas.pack()
        self.sketch_canvas.create_text(210, 150, text="加载中...", font=("Microsoft YaHei", 16), fill="gray", tags="placeholder")

        # Hint bar
        hint_bar = tk.Frame(self, bg=BG)
        hint_bar.pack(fill="x", padx=15)
        tk.Button(hint_bar, text="提示", font=("Microsoft YaHei", 11),
                  bg="#F39C12", fg="white", relief="flat", padx=12,
                  command=self._show_hint).pack(side="left")
        self.hint_label = tk.Label(hint_bar, text="", font=("Microsoft YaHei", 11), bg=BG, fg="#7F8C8D")
        self.hint_label.pack(side="left", padx=10)

        # Guess input row
        input_frame = tk.Frame(self, bg=BG)
        input_frame.pack(pady=8)
        tk.Label(input_frame, text="你的答案:", font=("Microsoft YaHei", 12), bg=BG, fg=DARK).pack(side="left")
        self.guess_entry = tk.Entry(input_frame, font=("Microsoft YaHei", 14), width=12,
                                    relief="solid", bd=1)
        self.guess_entry.pack(side="left", padx=5)
        self.guess_entry.bind("<Return>", lambda e: self._submit_guess())
        tk.Button(input_frame, text="提交", font=("Microsoft YaHei", 11, "bold"),
                  bg=ACCENT, fg="white", relief="flat", padx=12,
                  command=self._submit_guess).pack(side="left", padx=5)

        # Result area
        self.result_label = tk.Label(self, text="", font=("Microsoft YaHei", 14), bg=BG)
        self.result_label.pack(pady=3)

        # Next button (hidden initially)
        self.next_btn = tk.Button(self, text="下一题", font=("Microsoft YaHei", 11),
                                  bg=ACCENT, fg="white", relief="flat", padx=12,
                                  command=self._new_round)

        self.timer = CountdownTimer(self.winfo_toplevel(), self.timer_label, on_timeout=self._on_timeout)

    def _get_available_sketches(self):
        return get_all_sketchable_words()

    def _new_round(self):
        self.next_btn.pack_forget()
        self.result_label.config(text="")
        self.hint_label.config(text="")
        self.guess_entry.delete(0, "end")
        self.score_label.config(text=f"得分: {self.score_mgr.total}")

        available = self._get_available_sketches()
        if not available:
            # No local/cache sketches — pick any word and try to fetch
            available = [e["word"] for e in ALL_WORDS]

        word = random.choice(available)
        self.current_word = word
        self.current_word_entry = None
        for entry in ALL_WORDS:
            if entry["word"] == word:
                self.current_word_entry = entry
                break

        # Show loading
        self.sketch_canvas.delete("all")
        self.sketch_canvas.create_text(210, 150, text="加载中...",
                                       font=("Microsoft YaHei", 16), fill="gray")
        self.update()

        path, source = get_sketch_path(word)
        if not path:
            self.sketch_canvas.delete("all")
            self.sketch_canvas.create_text(210, 150, text=f"无法加载「{word}」的简笔画",
                                           font=("Microsoft YaHei", 14), fill="red")
            return

        try:
            img = Image.open(path)
            img = img.resize((420, 300), Image.LANCZOS)
            self.sketch_photo = ImageTk.PhotoImage(img)
            self.sketch_canvas.delete("all")
            self.sketch_canvas.create_image(0, 0, anchor="nw", image=self.sketch_photo)
            # Show source indicator
            source_text = {"local": "本地", "cache": "缓存", "online": "在线"}.get(source, "")
            if source_text:
                self.sketch_canvas.create_text(410, 290, text=source_text,
                                               font=("Microsoft YaHei", 8), fill="gray", anchor="se")
        except Exception as e:
            self.sketch_canvas.delete("all")
            self.sketch_canvas.create_text(210, 150, text=f"加载失败: {e}",
                                           font=("Microsoft YaHei", 14), fill="red")
            return

        self.timer.start()
        self.guess_entry.focus_set()

    def _show_hint(self):
        if self.current_word_entry:
            hint = get_hint(self.current_word_entry)
            self.hint_label.config(text=hint)
        else:
            # Word not in our list, give generic hint
            self.hint_label.config(text=f"共 {len(self.current_word)} 个字")

    def _submit_guess(self):
        guess = self.guess_entry.get().strip()
        if not guess:
            return

        self.timer.stop()
        correct = (guess == self.current_word)

        if correct:
            earned = self.score_mgr.add_correct(self.timer.remaining)
            self.result_label.config(text=f"正确! +{earned}分", fg=GREEN)
        else:
            self.score_mgr.add_wrong()
            self.result_label.config(text=f"错误! 正确答案: {self.current_word}", fg=RED)

        self.score_label.config(text=f"得分: {self.score_mgr.total}")
        self.next_btn.pack(pady=8)

    def _on_timeout(self):
        self.score_mgr.add_wrong()
        self.result_label.config(text=f"时间到! 答案: {self.current_word}", fg=RED)
        self.score_label.config(text=f"得分: {self.score_mgr.total}")
        self.next_btn.pack(pady=8)

    def _go_back(self):
        self.timer.stop()
        if self.on_back:
            self.on_back()
