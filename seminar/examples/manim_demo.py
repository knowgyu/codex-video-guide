"""The same two-second movement, rendered by Manim's animation engine."""
from manim import Scene, Dot, Line, LEFT, RIGHT, linear


class MovingDot(Scene):
    def construct(self):
        self.camera.background_color = '#e9f2f3'
        line = Line(LEFT * 4, RIGHT * 4, color='#a3bfc1')
        dot = Dot(LEFT * 4, radius=.35, color='#008c82')
        self.add(line, dot)
        self.play(dot.animate.move_to(RIGHT * 4), run_time=2, rate_func=linear)
