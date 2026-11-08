"""Create a two-second sequence of a dot moving across the screen."""
from pathlib import Path

from PIL import Image, ImageDraw

FPS = 60
SECONDS = 2
OUT = Path(__file__).resolve().parent / "frames"
OUT.mkdir(exist_ok=True)

for n in range(FPS * SECONDS):
    t = n / FPS
    x = 160 + 320 * t
    image = Image.new("RGB", (960, 540), "#e9f2f3")
    draw = ImageDraw.Draw(image)
    draw.line((160, 270, 800, 270), fill="#a3bfc1", width=4)
    draw.ellipse((x - 28, 242, x + 28, 298), fill="#008c82")
    image.save(OUT / f"frame_{n:04}.png")

print(f"Saved {FPS * SECONDS} frames to {OUT}")
