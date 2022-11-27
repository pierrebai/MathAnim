import anim

from math import modf as _modf
from typing import List as _List

class runner(anim.circle):
    runners: _List[anim.circle] = []
    runnings: _List[anim.circle] = []
    runners_count: int = 0
    lonely: anim.circle = None
    lonely_zone_size: float = 0.5
    track_radius: float = 1.
    always_colored = False

    @staticmethod
    def create_runners(speeds: _List[int], lonely_index: int, runner_size: float, track_radius: float, label_size: float) -> None:
        runner.track_radius = track_radius
        runner.runners = [runner(speed, runner_size, label_size) for speed in speeds]
        runner.lonely = runner.runners[lonely_index]
        runner.runnings = [r for r in runner.runners if r != runner.lonely] 
        runner.runners_count = len(runner.runners)
        runner.lonely_zone_size = 1. / runner.runners_count

    def __init__(self, speed: float, runner_size: float, label_size: float):
        self.speed = speed
        self.lap_fraction = 0.
        self.colored = False
        self.label = None
        super().__init__(anim.radial_point(anim.origin, runner.track_radius, anim.hpi), runner_size)
        self.label = anim.scaling_text(f'{int(self.speed)}', self.center, label_size).set_opacity(0.)
        self.reset()

    def reset(self):
        self.lap_fraction = 0.
        self.colored = False
        self.fill(anim.white).set_opacity(0.)
        self._update_geometry()

    @staticmethod
    def _normalize_lap_fraction(fraction: float) -> float:
        fraction =_modf(fraction)[0]
        if fraction < 0.:
            return 1. + fraction
        else:
            return fraction

    def set_opacity(self, opacity) -> anim.circle:
        self.label.set_opacity(opacity)
        return super().set_opacity(opacity)

    def set_lap_fraction(self, fraction: float):
        self.lap_fraction = runner._normalize_lap_fraction(fraction)
        self.center.set_angle(anim.hpi + anim.tau * self.lap_fraction)
        return self

    def distance_from_lonely(self):
        return runner._normalize_lap_fraction(self.lap_fraction - runner.lonely.lap_fraction)

    def anim_lap_fraction(self):
        return lambda f : self.set_lap_fraction(f)

    def is_nearest_left(self) -> bool:
        if self == runner.lonely:
            return False
        return self == min(runner.runnings, key=lambda r: r.distance_from_lonely())

    def is_nearest_right(self) -> bool:
        if self == runner.lonely:
            return False
        return self == max(runner.runnings, key=lambda r: r.distance_from_lonely())

    def is_lonely(self) -> bool:
        return self == runner.lonely

    def is_in_lonely_zone(self) -> bool:
        distance = self.distance_from_lonely()
        return distance < runner.lonely_zone_size or distance > 1. - runner.lonely_zone_size

    def set_colored(self, colored: bool):
        self.colored = colored
        self.update_color()
        return self

    def update_color(self) -> anim.circle:
        if not self.colored:
            return
        elif self.is_lonely():
            color = anim.blue
        elif self.is_in_lonely_zone():
            color = anim.red
        elif self.is_nearest_left():
            color = anim.yellow
        elif self.is_nearest_right():
            color = anim.yellow
        else:
            color = anim.green
        return self.fill(color)

    def update_label(self) -> anim.circle:
        if self.label:
            self.label.center_on(self)
        return self

    def _update_geometry(self):
        super()._update_geometry()
        self.update_label()
        if runner.runners:
            if runner.always_colored or self == runner.runners[-1]:
                for r in runner.runners:
                    r.update_color()

