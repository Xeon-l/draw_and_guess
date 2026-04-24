"""Generate simple placeholder sketch images for guess mode."""
import os
from PIL import Image, ImageDraw, ImageFont

SKETCH_DIR = os.path.join(os.path.dirname(__file__), "assets", "sketches")
os.makedirs(SKETCH_DIR, exist_ok=True)

SKETCHES = {
    "猫": lambda d: _draw_cat(d),
    "狗": lambda d: _draw_dog(d),
    "鱼": lambda d: _draw_fish(d),
    "太阳": lambda d: _draw_sun(d),
    "树": lambda d: _draw_tree(d),
    "房子": lambda d: _draw_house(d),
    "花": lambda d: _draw_flower(d),
    "苹果": lambda d: _draw_apple(d),
    "星星": lambda d: _draw_star(d),
    "月亮": lambda d: _draw_moon(d),
    "汽车": lambda d: _draw_car(d),
    "雨伞": lambda d: _draw_umbrella(d),
    "杯子": lambda d: _draw_cup(d),
    "帽子": lambda d: _draw_hat(d),
    "钥匙": lambda d: _draw_key(d),
    "自行车": lambda d: _draw_bike(d),
    "飞机": lambda d: _draw_plane(d),
    "船": lambda d: _draw_boat(d),
    "灯泡": lambda d: _draw_bulb(d),
    "剪刀": lambda d: _draw_scissors(d),
}


def _text_label(draw, text, y=260):
    """No-op: do not draw answer on sketch."""
    pass


def _draw_cat(d):
    # Body
    d.ellipse([120, 120, 280, 240], outline="black", width=3)
    # Head
    d.ellipse([160, 60, 240, 140], outline="black", width=3)
    # Ears
    d.polygon([(170, 80), (160, 40), (190, 70)], outline="black", width=3)
    d.polygon([(230, 80), (240, 40), (210, 70)], outline="black", width=3)
    # Eyes
    d.ellipse([180, 90, 195, 105], fill="black")
    d.ellipse([205, 90, 220, 105], fill="black")
    # Tail
    d.arc([270, 140, 320, 200], 270, 90, fill="black", width=3)
    _text_label(d, "猫")


def _draw_dog(d):
    # Body
    d.ellipse([110, 130, 290, 250], outline="black", width=3)
    # Head
    d.ellipse([150, 50, 250, 150], outline="black", width=3)
    # Ears (floppy)
    d.ellipse([130, 50, 165, 110], outline="black", width=3)
    d.ellipse([235, 50, 270, 110], outline="black", width=3)
    # Eyes
    d.ellipse([175, 85, 190, 100], fill="black")
    d.ellipse([210, 85, 225, 100], fill="black")
    # Nose
    d.ellipse([190, 110, 210, 125], fill="black")
    # Tail
    d.line([(280, 180), (320, 140)], fill="black", width=3)
    _text_label(d, "狗")


def _draw_fish(d):
    # Body
    d.ellipse([100, 100, 300, 200], outline="black", width=3)
    # Tail
    d.polygon([(300, 150), (350, 100), (350, 200)], outline="black", width=3)
    # Eye
    d.ellipse([140, 125, 160, 145], fill="black")
    # Fin
    d.arc([160, 180, 220, 230], 0, 180, fill="black", width=3)
    _text_label(d, "鱼")


def _draw_sun(d):
    # Center
    d.ellipse([140, 100, 260, 220], outline="black", width=3)
    # Rays
    import math
    cx, cy, r = 200, 160, 80
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = cx + int(r * math.cos(rad))
        y1 = cy + int(r * math.sin(rad))
        x2 = cx + int((r + 40) * math.cos(rad))
        y2 = cy + int((r + 40) * math.sin(rad))
        d.line([(x1, y1), (x2, y2)], fill="black", width=3)
    _text_label(d, "太阳")


def _draw_tree(d):
    # Trunk
    d.rectangle([180, 180, 220, 260], outline="black", width=3)
    # Crown
    d.ellipse([120, 60, 280, 200], outline="black", width=3)
    _text_label(d, "树")


def _draw_house(d):
    # Base
    d.rectangle([120, 130, 280, 250], outline="black", width=3)
    # Roof
    d.polygon([(100, 130), (200, 50), (300, 130)], outline="black", width=3)
    # Door
    d.rectangle([175, 180, 225, 250], outline="black", width=3)
    # Window
    d.rectangle([135, 150, 165, 180], outline="black", width=3)
    d.rectangle([235, 150, 265, 180], outline="black", width=3)
    _text_label(d, "房子")


def _draw_flower(d):
    # Stem
    d.line([(200, 160), (200, 260)], fill="black", width=3)
    # Petals
    import math
    cx, cy = 200, 120
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        px = cx + int(40 * math.cos(rad))
        py = cy + int(40 * math.sin(rad))
        d.ellipse([px - 20, py - 20, px + 20, py + 20], outline="black", width=2)
    # Center
    d.ellipse([185, 105, 215, 135], fill="yellow", outline="black", width=2)
    _text_label(d, "花")


def _draw_apple(d):
    d.ellipse([140, 80, 260, 220], outline="black", width=3)
    # Stem
    d.line([(200, 80), (210, 50)], fill="black", width=3)
    # Leaf
    d.arc([205, 45, 235, 75], 0, 180, fill="green", width=2)
    _text_label(d, "苹果")


def _draw_star(d):
    import math
    cx, cy, r = 200, 130, 60
    points = []
    for i in range(5):
        angle = math.radians(90 + i * 72)
        points.append((cx + int(r * math.cos(angle)), cy - int(r * math.sin(angle))))
        angle2 = math.radians(90 + i * 72 + 36)
        points.append((cx + int(r * 0.4 * math.cos(angle2)), cy - int(r * 0.4 * math.sin(angle2))))
    d.polygon(points, outline="black", width=3)
    _text_label(d, "星星")


def _draw_moon(d):
    d.arc([100, 50, 300, 250], 200, 340, fill="black", width=5)
    d.arc([130, 50, 300, 230], 210, 330, fill="black", width=5)
    _text_label(d, "月亮")


def _draw_car(d):
    # Body
    d.rectangle([100, 140, 300, 200], outline="black", width=3)
    # Top
    d.rectangle([140, 90, 260, 140], outline="black", width=3)
    # Wheels
    d.ellipse([120, 190, 170, 240], outline="black", width=3)
    d.ellipse([230, 190, 280, 240], outline="black", width=3)
    _text_label(d, "汽车")


def _draw_umbrella(d):
    # Handle
    d.line([(200, 100), (200, 240)], fill="black", width=3)
    d.arc([170, 220, 200, 250], 0, 180, fill="black", width=3)
    # Canopy
    d.arc([100, 60, 300, 200], 180, 360, fill="black", width=4)
    _text_label(d, "雨伞")


def _draw_cup(d):
    d.rectangle([140, 100, 260, 220], outline="black", width=3)
    # Handle
    d.arc([255, 130, 295, 190], 270, 90, fill="black", width=3)
    _text_label(d, "杯子")


def _draw_hat(d):
    # Brim
    d.ellipse([110, 160, 290, 200], outline="black", width=3)
    # Top
    d.rectangle([140, 80, 260, 160], outline="black", width=3)
    _text_label(d, "帽子")


def _draw_key(d):
    # Ring
    d.ellipse([120, 80, 180, 140], outline="black", width=3)
    # Shaft
    d.line([(180, 110), (300, 110)], fill="black", width=3)
    # Teeth
    d.line([(280, 110), (280, 140)], fill="black", width=3)
    d.line([(260, 110), (260, 135)], fill="black", width=3)
    _text_label(d, "钥匙")


def _draw_bike(d):
    # Wheels
    d.ellipse([100, 130, 180, 210], outline="black", width=3)
    d.ellipse([220, 130, 300, 210], outline="black", width=3)
    # Frame
    d.line([(140, 170), (200, 120)], fill="black", width=3)
    d.line([(200, 120), (260, 170)], fill="black", width=3)
    d.line([(140, 170), (260, 170)], fill="black", width=3)
    # Handlebars
    d.line([(200, 120), (200, 90)], fill="black", width=3)
    d.line([(180, 90), (220, 90)], fill="black", width=3)
    _text_label(d, "自行车")


def _draw_plane(d):
    # Body
    d.ellipse([80, 130, 320, 170], outline="black", width=3)
    # Wings
    d.polygon([(160, 150), (200, 80), (240, 150)], outline="black", width=3)
    # Tail
    d.polygon([(80, 150), (60, 100), (100, 150)], outline="black", width=3)
    _text_label(d, "飞机")


def _draw_boat(d):
    # Hull
    d.polygon([(100, 180), (300, 180), (270, 230), (130, 230)], outline="black", width=3)
    # Mast
    d.line([(200, 60), (200, 180)], fill="black", width=3)
    # Sail
    d.polygon([(200, 70), (280, 140), (200, 140)], outline="black", width=3)
    _text_label(d, "船")


def _draw_bulb(d):
    # Bulb shape
    d.ellipse([140, 50, 260, 180], outline="black", width=3)
    # Base
    d.rectangle([160, 180, 240, 220], outline="black", width=3)
    d.line([(160, 195), (240, 195)], fill="black", width=2)
    d.line([(160, 210), (240, 210)], fill="black", width=2)
    # Rays
    d.line([(200, 30), (200, 10)], fill="black", width=2)
    d.line([(280, 80), (300, 70)], fill="black", width=2)
    d.line([(120, 80), (100, 70)], fill="black", width=2)
    _text_label(d, "灯泡")


def _draw_scissors(d):
    # Handle circles
    d.ellipse([80, 140, 140, 200], outline="black", width=3)
    d.ellipse([80, 100, 140, 160], outline="black", width=3)
    # Blades
    d.line([(140, 170), (280, 80)], fill="black", width=3)
    d.line([(140, 130), (280, 80)], fill="black", width=3)
    _text_label(d, "剪刀")


def main():
    for word, draw_fn in SKETCHES.items():
        img = Image.new("RGB", (400, 300), "white")
        draw = ImageDraw.Draw(img)
        draw_fn(draw)
        path = os.path.join(SKETCH_DIR, f"{word}.png")
        img.save(path)
        print(f"Generated: {word}.png")

    print(f"\nGenerated {len(SKETCHES)} sketch images in {SKETCH_DIR}")


if __name__ == "__main__":
    main()
