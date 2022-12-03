import anim

from math import modf as _modf
from typing import List as _List

class runner(anim.circle):
    '''
    Hold all information about a runner, used to illustrate the
    lonely runner hypothesis.
    '''
    speeds: _List[float] = []          # Runners speeds
    runners: _List[anim.circle] = []    # All runners
    runnings: _List[anim.circle] = []   # Runners except the lonely runner
    runners_count: int = 0              # How many runners there are, just len(runners)
    lonely: anim.circle = None          # The lonely runner
    lonely_zone_size: float = 0.5       # The lonely zone size: 1  / runners_count
    always_colored = False              # Force all runners to update their colors

    @classmethod
    def create_runners(clazz, speeds: _List[int], lonely_index: int, runner_size: float, track_radius: float) -> None:
        '''
        Creates all the runners corresponding to the given speeds and which
        runner we want to isolate to be lonely.
        '''
        runner.speeds = speeds
        runner.runners = []
        for speed in speeds:
            runner.runners.append(clazz(speed, track_radius, runner_size, runner_size * 3. / 4.))
        runner.lonely = runner.runners[lonely_index]
        runner.runnings = [r for r in runner.runners if r != runner.lonely] 
        runner.runners_count = len(runner.runners)
        runner.lonely_zone_size = 1. / runner.runners_count

    def __init__(self, speed: float, track_radius: float, runner_size: float, label_size: float):
        '''
        Initializes the runner speed, position, colored flag, label, etc.
        '''
        self.speed = speed
        self.lap_fraction = 0.
        self.colored = False
        self.label = None
        super().__init__(anim.radial_point(anim.origin, track_radius, anim.hpi), runner_size)
        self.label = anim.scaling_text(f'{int(self.speed)}', self.center, label_size)
        self.reset()

    def reset(self):
        '''
        Resets the runner position, its colored flag, and its fill color.
        '''
        self.lap_fraction = 0.
        self.colored = False
        self.fill(anim.white)
        self._update_geometry()

    @staticmethod
    def _normalize_lap_fraction(fraction: float) -> float:
        '''
        Return the fraction of a lap constrained between 0 and 1.
        '''
        fraction =_modf(fraction)[0]
        if fraction < 0.:
            return 1. + fraction
        else:
            return fraction

    def set_opacity(self, opacity) -> anim.circle:
        '''
        Sets the runner illiustrated opacity, and the opcaity of its label.
        '''
        self.label.set_opacity(opacity)
        return super().set_opacity(opacity)

    def set_lap_fraction(self, fraction: float):
        '''
        Sets the position of the runner around the track as a fraction
        of a lap, between 0 and 1. Updates the illustration.
        '''
        self.lap_fraction = runner._normalize_lap_fraction(fraction)
        self.center.set_angle(anim.hpi + anim.tau * self.lap_fraction)
        return self

    def distance_from(self, r) -> float:
        '''
        Returns the distance from this runner to another runner as a
        fraction of a lap, between 0 and 0.5
        '''
        frac = runner._normalize_lap_fraction(self.lap_fraction - r.lap_fraction)
        if frac > 0.5:
            frac = 1. - frac
        return frac

    def distance_from_lonely(self):
        '''
        Returns the distance from this runner to the lonely runner as a
        fraction of a lap, between 0 and 0.5
        '''
        return self.distance_from(runner.lonely)

    def anim_lap_fraction(self):
        '''
        Returns a functions that can animate the lap fraction of this runner.
        '''
        return lambda f : self.set_lap_fraction(f)

    def is_nearest_left(self) -> bool:
        '''
        Returns true if this runner is the nearest runner to the left of the
        lonely runner.
        '''
        if self == runner.lonely:
            return False
        return self == min(runner.runnings, key=lambda r: r.distance_from_lonely())

    def is_nearest_right(self) -> bool:
        '''
        Returns true if this runner is the nearest runner to the right of the
        lonely runner.
        '''
        if self == runner.lonely:
            return False
        return self == max(runner.runnings, key=lambda r: r.distance_from_lonely())

    def is_lonely(self) -> bool:
        '''
        Returns true if this runner is the lonely runner.
        '''
        return self == runner.lonely

    def is_in_lonely_zone(self) -> bool:
        '''
        Returns true if this runner is in the lonely runner exclusion zone.
        '''
        distance = self.distance_from_lonely()
        return distance < runner.lonely_zone_size

    def set_colored(self, colored: bool):
        '''
        Sets if this runner should be drawn with colors.
        '''
        self.colored = colored
        self._update_lonely_status()
        return self

    def _update_lonely_status(self) -> anim.circle:
        '''
        Updates the color of this runner based on the colored flags and the
        position of the runner vs the lonely runner.
        '''
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

    def _update_label(self) -> anim.circle:
        '''
        Updates the position of the label to be on top of the runner.
        '''
        if self.label:
            self.label.center_on(self)
        return self

    def _update_geometry(self):
        '''
        Updates the runner illustration when its geometry has changed.
        '''
        super()._update_geometry()
        self._update_label()
        if runner.runners:
            if runner.always_colored or self == runner.runners[-1]:
                for r in runner.runners:
                    r._update_lonely_status()

