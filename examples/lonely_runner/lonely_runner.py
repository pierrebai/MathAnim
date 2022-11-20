import anim
from typing import List as _List
from .runners_allowed_intervals import *

#################################################################
#
# Description

name = 'Lonely Runner'
description = 'https://en.wikipedia.org/wiki/Lonely_runner_conjecture'
loop = False
reset_on_change = True
has_pointing_arrow = True


#################################################################
#
# Options

runners_speeds_options = anim.option('Runner speeds', 'The runner speeds, a list of integers.', '0 1 3 4 7', '', '')
lonely_runner_options = anim.option('Lonely Runner', 'The runner index, starting from zero, that will be lonely.', 0, 0, 100)

def runners_speeds() -> _List[int]:
    return [int(s) for s in runners_speeds_options.value.split()]

def lonely_runner_index() -> int:
    return int(lonely_runner_options.value)

def runners_count() -> int:
    return len(runners_speeds())

def reset(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    animation.current_shot_index = -1


#################################################################
#
# Points and geometries

track_radius: float = 500.
dot_size: float = 40.

runners: _List[anim.circle] = []
runners_inclusion_zones: _List[anim.rectangle] = []

track = anim.circle(anim.point(0., 0.), track_radius).thickness(dot_size * 2.5).outline(anim.sable).set_opacity(0.)
track_label = anim.scaling_text('1', anim.point(0., 0.), 200.).set_opacity(0.)

timeline_offset = 300.

timeline = anim.line(
    anim.point( -track_radius, timeline_offset),
    anim.point( track_radius, timeline_offset)).thickness(dot_size).set_opacity(0.)

timeline_labels = [
    anim.scaling_text('0', timeline.p1, 80.).set_opacity(0.),
    anim.scaling_text('1', timeline.p2, 80.).set_opacity(0.),
]

def lonely_runner() -> anim.circle:
    return runners[lonely_runner_index()]

def _make_runner(runner_speed: int) -> anim.circle:
    return anim.circle(anim.point(0., track_radius), dot_size).fill(anim.black).set_opacity(0.)

def _gen_runners():
    global runners
    runners = [_make_runner(speed) for speed in runners_speeds()]


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    _gen_runners()

    actors = [
        [anim.actor('Runner', '', rd) for rd in runners],
        anim.actor('Track', '', track),
        anim.actor('Label', '', track_label),
        [anim.actor('Label', '', label) for label in timeline_labels],
        anim.actor('Timeline', '', timeline),
    ]
    animation.add_actors(actors, scene)
    rect_radius =  track_radius + 50
    scene.add_item(anim.create_invisible_rect(-rect_radius, -rect_radius, rect_radius * 2, rect_radius * 4))

def generate_runner_inclusion_zone(animation: anim.animation, scene: anim.scene, runner, runner_zones):
    pass


#################################################################
#
# Prepare animation

def _reset_opacities() -> None:
    for item in anim.find_all_of_type(globals(), anim.item):
        item.set_opacity(0.)

def _reposition_points() -> None:
    for pt in anim.find_all_of_type(globals(), anim.point):
        pt.reset()
    for circle in anim.find_all_of_type(globals(), anim.circle):
        circle.center.reset()

def _remove_zones(animation: anim.animation, scene: anim.scene) -> None:
    global runners_inclusion_zones
    for zone in runners_inclusion_zones:
        animation.remove_actor(zone, scene)
    runners_inclusion_zones = []

def _raise_runners():
    for runner in runners:
        runner.setZValue(1.)

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator) -> None:
    _reset_opacities()
    _reposition_points()
    _remove_zones(animation, scene)
    _raise_runners()

def reset(animation: anim.animation, scene: anim.scene, animator: anim.animator) -> None:
    prepare_playing(animation, scene, animator)


#################################################################
#
# Shots

duration = 3.
arrow_duration = duration / 10.

def show_track_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Running track

    Imagine a track around
    which runners make laps.
    '''
    animator.animate_value([0., 1.], duration / 4., anim.reveal_item(track))
    animation.anim_pointing_arrow(track.get_circumference_point(-0.4), arrow_duration, scene, animator)

def measure_track_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Running track

    For simplicity, we will
    assume that the length
    of the track is one,
    in some arbitrary units.
    '''
    track_label.center_on(track)
    animator.animate_value([0., 1.], duration / 4., anim.reveal_item(track_label))
    animation.anim_pointing_arrow(track.get_circumference_point(-0.4), arrow_duration, scene, animator)

def introduce_runners_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Runners

    Many runners are making
    laps around the circular
    track.
    '''
    count = runners_count()
    for i, runner in zip(range(count), runners):
        opacities = [0.] + [0.] * i + [1.] * (count - i)
        animator.animate_value(opacities, duration, anim.reveal_item(runner))

        angles = [0.] + [i * 15.] * (count - i)
        animator.animate_value(angles, duration, anim.rotate_point_around(runner.center, track.center))
    animation.attach_pointing_arrow(runners[-1].center, scene)
    #animation.anim_pointing_arrow([anim.relative_point(runner.center) for runner in runners], duration, scene, animator)

def show_runners_running_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Runners

    Each one runs at their
    own speed. All speeds
    are different.
    '''
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., 360. * speed], duration, anim.rotate_point_around(runner.center, track.center))
    animation.attach_pointing_arrow(runners[1].center, scene)

def lonely_runner_theorem_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Lonely Runner Theorem

    The lonely runner theorem
    claims that each runner
    will eventually be lonely
    at some time.
    '''
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., 360. * speed], duration, anim.rotate_point_around(runner.center, track.center))

def lonely_runner_separation_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Lonely?

    A runner is lonely if all
    other runners are far
    enough. This distance is
    defined as one over the
    number of runners.

    (Given that the track
    circumference is one.)
    '''
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., 360. * speed], duration, anim.rotate_point_around(runner.center, track.center))

def lonely_runner_unproven_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Unproven

    The lonely runner theorem
    is not proven...
    '''
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., 360. * speed], duration, anim.rotate_point_around(runner.center, track.center))

def lonely_runner_theorem_simplications_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Simplifications

    ... while unproven, some
    simplifications have been
    shown to be equivalent to
    the general theorem.
    '''
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., 360. * speed], duration, anim.rotate_point_around(runner.center, track.center))

def lonely_runner_theorem_speeds_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Integer speeds

    For example, the speeds
    can all be integers, they
    can all be positive and
    one speed can be set to
    zero.
    '''
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., 360. * speed], duration, anim.rotate_point_around(runner.center, track.center))


#################################################################
#
# Animation

lonely_runner = anim.simple_animation.from_module(globals())
