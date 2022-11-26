import anim

from math import modf as _modf
from typing import List as _List

class runner(anim.circle):
    runners: _List = []
    runnings: _List = []
    runners_count: int = 0
    lonely = None
    lonely_zone_size: float = 0.5
    track_radius: float = 1.

    @staticmethod
    def create_runners(speeds: _List[int], lonely_index, runner_size, track_radius) -> None:
        runner.track_radius = track_radius
        runner.runners = [runner(speed, runner_size) for speed in speeds]
        runner.runnings = [r for r in runner.runners if r.speed != 0.] 
        runner.runners_count = len(runner.runners)
        runner.lonely = runner.runners[lonely_index]
        runner.lonely_zone_size = 1. / runner.runners_count

    def __init__(self, speed: float, runner_size: float):
        self.speed = speed
        self.lap_fraction = 0.
        self.colored = False
        super().__init__(anim.point(0., runner.track_radius), runner_size)
        self.reset()

    def reset(self):
        self.lap_fraction = 0.
        self.colored = False
        self.fill(anim.white).set_opacity(0.)

    def set_lap_fraction(self, fraction: float):
        self.lap_fraction = _modf(fraction)[0]
        self.center.set_point(
            anim.create_relative_point_around_center(anim.origin, runner.track_radius, anim.pi / 2 + anim.tau * self.lap_fraction)
        )
        return self

    def anim_lap_fraction(self):
        return lambda f : self.set_lap_fraction(f)

    def is_nearest_left(self) -> bool:
        if self == runner.lonely:
            return False
        return self == min(runner.runnings, key=lambda r: r.lap_fraction)

    def is_nearest_right(self) -> bool:
        if self == runner.lonely:
            return False
        return self == max(runner.runnings, key=lambda r: r.lap_fraction)

    def is_lonely(self) -> bool:
        return self == runner.lonely

    def in_lonely_zone(self) -> bool:
        return self.lap_fraction < runner.lonely_zone_size or self.lap_fraction > 1. - runner.lonely_zone_size

    def set_colored(self, colored: bool):
        self.colored = colored
        self.update_color()
        return self

    def update_color(self):
        if not self.colored:
            color = anim.white
        elif self.is_lonely():
            color = anim.blue
        elif self.in_lonely_zone():
            color = anim.red
        elif self.is_nearest_left():
            color = anim.yellow
        elif self.is_nearest_right():
            color = anim.yellow
        else:
            color = anim.green
        return self.fill(color)

    def _update_geometry(self):
        super()._update_geometry()
        if runner.runnings and self == runner.runnings[-1]:
            for r in runner.runnings:
                r.update_color()

