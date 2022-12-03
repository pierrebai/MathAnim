import anim
from typing import List as _List
from .runners_allowed_intervals import *
from .runner import runner

#################################################################
#
# Description

name = 'Lonely Runner - Sinplified'
description = 'https://en.wikipedia.org/wiki/Lonely_runner_conjecture'
loop = True
reset_on_change = True
has_pointing_arrow = False


#################################################################
#
# Options

runners_speeds_options = anim.option('Runner speeds', 'The runner speeds, a list of integers.', '0 1 3 4 7', '', '')
lonely_runner_options = anim.option('Lonely Runner', 'The runner index, starting from zero, that will be lonely.', 0, 0, 100)

def runners_speeds() -> _List[float]:
    try:
        return [float(s) for s in runners_speeds_options.value.split()]
    except ValueError:
        return [0]

def lonely_runner_index() -> int:
    return min(int(lonely_runner_options.value), len(runners_speeds()))


#################################################################
#
# Runner with lonely detection

class lonely_runner(runner):
    def __init__(self, *args):
        self.interval_arc = None
        self._fill_intervals()
        super().__init__(*args)
        self._create_interval_arc()

    def _fill_intervals(self):
        lonely_index = len(runner.runners)
        self.lonely_intervals = runners_solution(
            runner.speeds, lonely_index).intervals

    def _create_interval_arc(self):
        lonely_angle = anim.tau * runner.lonely_zone_size
        pt1 = anim.relative_radial_point(self.center, 0., -lonely_angle)
        pt2 = anim.relative_radial_point(self.center, 0.,  lonely_angle)
        self.interval_arc = anim.partial_circle(self.center, self.radius, pt1, pt2).fill(anim.no_color).outline(anim.black)

    def is_lonely(self) -> bool:
        closest = min([self.distance_from(r) for r in lonely_runner.runners if r != self])
        return closest >= runner.lonely_zone_size - 0.01

    def _update_lonely_status(self) -> anim.circle:
        if self.is_lonely():
            color = anim.blue
            self.interval_arc.set_opacity(1.)
        else:
            color = anim.white
            self.interval_arc.set_opacity(0.)
        return self.fill(color)


#################################################################
#
# Points and geometries

runner_radius: float = 40.
track_radius: float = 500.
track_width: float = runner_radius * 2.5

track = anim.circle(anim.origin, track_radius).thickness(track_width).outline(anim.sable)
track.setZValue(-1.)

def _gen_runners():
    lonely_runner.create_runners(runners_speeds(), lonely_runner_index(), runner_radius, track_radius)
    for r in lonely_runner.runners:
        r.set_colored(True)
        r.label.setZValue(2.)
        r.interval_arc.setZValue(4.)


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    _gen_runners()

    actors = [
        [anim.actor('Runner', '', r) for r in runner.runners],
        [anim.actor('Label', '', r.label) for r in runner.runners],
        anim.actor('Track', '', track),
    ]
    animation.add_actors(actors, scene)
    rect_radius = track_radius * 1.1
    scene.add_item(anim.create_invisible_rect(-rect_radius, -rect_radius, rect_radius * 2, rect_radius * 2))


#################################################################
#
# Shots

def running_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Lonely Runners
    '''
    for r in runner.runners:
        animator.animate_value([0., r.speed], 30., r.anim_lap_fraction())


#################################################################
#
# Animation

lonely_runner_sinplified = anim.simple_animation.from_module(globals())
