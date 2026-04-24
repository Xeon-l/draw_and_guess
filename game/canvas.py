"""Drawing canvas widget with freehand drawing, colors, undo, clear."""
import tkinter as tk
from PIL import Image, ImageDraw


COLORS = [
    ("黑色", "#000000"),
    ("红色", "#FF0000"),
    ("蓝色", "#0066FF"),
    ("绿色", "#00CC00"),
    ("黄色", "#FFCC00"),
    ("紫色", "#9933FF"),
    ("橙色", "#FF6600"),
    ("棕色", "#996633"),
]

BRUSH_SIZES = [("细", 2), ("中", 5), ("粗", 10)]


class DrawingCanvas(tk.Frame):
    def __init__(self, master, width=500, height=400, **kwargs):
        super().__init__(master, **kwargs)
        self.width = width
        self.height = height
        self.current_color = "#000000"
        self.current_size = 5
        self.strokes = []  # list of strokes for undo
        self.current_stroke = []
        self._drawing = False

        self.canvas = tk.Canvas(self, width=width, height=height, bg="white",
                                cursor="cross", relief="sunken", bd=2)
        self.canvas.pack(pady=5)

        # Off-screen image for export
        self._image = Image.new("RGB", (width, height), "white")
        self._draw = ImageDraw.Draw(self._image)

        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        self._build_controls()

    def _build_controls(self):
        ctrl = tk.Frame(self)
        ctrl.pack(fill="x", padx=5)

        # Colors
        color_frame = tk.LabelFrame(ctrl, text="颜色")
        color_frame.pack(side="left", padx=5)
        for name, hex_color in COLORS:
            btn = tk.Button(color_frame, bg=hex_color, width=2, height=1,
                            command=lambda c=hex_color: self._set_color(c))
            btn.pack(side="left", padx=1)

        # Brush size
        size_frame = tk.LabelFrame(ctrl, text="画笔")
        size_frame.pack(side="left", padx=5)
        for name, size in BRUSH_SIZES:
            btn = tk.Button(size_frame, text=name, width=3,
                            command=lambda s=size: self._set_size(s))
            btn.pack(side="left", padx=1)

        # Actions
        action_frame = tk.Frame(ctrl)
        action_frame.pack(side="right", padx=5)
        tk.Button(action_frame, text="撤销", command=self.undo, width=6).pack(side="left", padx=2)
        tk.Button(action_frame, text="清空", command=self.clear, width=6).pack(side="left", padx=2)

    def _set_color(self, color):
        self.current_color = color

    def _set_size(self, size):
        self.current_size = size

    def _on_press(self, event):
        self._drawing = True
        self.current_stroke = [(event.x, event.y)]

    def _on_drag(self, event):
        if not self._drawing:
            return
        x, y = event.x, event.y
        if self.current_stroke:
            x0, y0 = self.current_stroke[-1]
            self.canvas.create_line(x0, y0, x, y,
                                    fill=self.current_color, width=self.current_size,
                                    capstyle="round", smooth=True)
            self._draw.line([(x0, y0), (x, y)],
                            fill=self.current_color, width=self.current_size)
        self.current_stroke.append((x, y))

    def _on_release(self, event):
        if self._drawing and self.current_stroke:
            self.strokes.append({
                "points": list(self.current_stroke),
                "color": self.current_color,
                "size": self.current_size,
            })
        self._drawing = False
        self.current_stroke = []

    def undo(self):
        if not self.strokes:
            return
        self.strokes.pop()
        self._redraw()

    def clear(self):
        self.strokes.clear()
        self._redraw()

    def _redraw(self):
        self.canvas.delete("all")
        self._image = Image.new("RGB", (self.width, self.height), "white")
        self._draw = ImageDraw.Draw(self._image)
        for stroke in self.strokes:
            points = stroke["points"]
            color = stroke["color"]
            size = stroke["size"]
            for i in range(1, len(points)):
                x0, y0 = points[i - 1]
                x1, y1 = points[i]
                self.canvas.create_line(x0, y0, x1, y1,
                                        fill=color, width=size, capstyle="round", smooth=True)
                self._draw.line([(x0, y0), (x1, y1)], fill=color, width=size)

    def get_image(self):
        """Return a copy of the current canvas as a PIL Image."""
        return self._image.copy()
