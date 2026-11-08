"""Render a moving dot as an actual sequence of Pillow PNG frames."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[2] / 'output/video-pipeline-v3/pillow'
OUT.mkdir(parents=True, exist_ok=True)
WIDTH, HEIGHT, FPS, SECONDS = 960, 540, 60, 2
font = ImageFont.truetype(str(Path(__file__).resolve().parents[2] / 'llm-film/fonts/Pretendard-Bold.otf'), 48)

for n in range(FPS * SECONDS):
    t = n / FPS
    x = 160 + 320 * t
    image = Image.new('RGB', (WIDTH, HEIGHT), '#e9f2f3')
    draw = ImageDraw.Draw(image)
    if n == 0:
        image.save(OUT / 'step_blank.png')
    draw.line((160, 270, 800, 270), fill='#a3bfc1', width=4)
    if n == 0:
        image.save(OUT / 'step_line.png')
    draw.ellipse((x-28, 242, x+28, 298), fill='#008c82')
    if n == 0:
        image.save(OUT / 'step_dot.png')
    draw.text((160, 65), '안녕하세요', font=font, fill='#173b49')
    image.save(OUT / f'frame_{n:04}.png')

print(f'Wrote {FPS * SECONDS} PNG frames to {OUT}')
