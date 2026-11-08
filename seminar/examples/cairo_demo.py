"""Draw a real Cairo vector path into raster PNG frames."""
from pathlib import Path
import cairo

OUT = Path(__file__).resolve().parents[2] / 'output/video-pipeline-v3/cairo'
OUT.mkdir(parents=True, exist_ok=True)
WIDTH, HEIGHT, FPS, SECONDS = 960, 540, 60, 2

for n in range(FPS * SECONDS):
    t = n / FPS
    x = 160 + 320 * t
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(.914, .949, .953)
    ctx.paint()
    ctx.set_source_rgb(.64, .75, .76)
    ctx.set_line_width(4)
    ctx.move_to(160, 270)
    ctx.line_to(800, 270)
    ctx.stroke()
    ctx.set_source_rgb(0, .55, .51)
    ctx.arc(x, 270, 28, 0, 6.283185307179586)
    ctx.fill()
    surface.write_to_png(str(OUT / f'frame_{n:04}.png'))

print(f'Wrote {FPS * SECONDS} PNG frames to {OUT}')
