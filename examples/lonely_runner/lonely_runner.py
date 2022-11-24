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

def lonely_zone_size() -> float:
    return anim.tau / runners_count()

def reset(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    animation.current_shot_index = -1


#################################################################
#
# Points and geometries

track_radius: float = 500.
track_center = anim.point(0., 0.)
dot_size: float = 40.
track_width: float = dot_size * 2.5
lonely_radius: float = track_radius + dot_size

track_label_size: float = 200.
timeline_label_size: float = 80.

runners_centers: _List[anim.point] = []
runners: _List[anim.circle] = []
runners_inclusion_zones: _List[anim.rectangle] = []

lonely_zone: anim.circle = None
lonely_space: anim.circle = None

track = anim.circle(track_center, track_radius).thickness(track_width).outline(anim.sable)
track_label = anim.scaling_text('1', track_center, track_label_size)

timeline_offset: float = 300.

timeline = anim.line(
    anim.point( -track_radius, timeline_offset),
    anim.point( track_radius, timeline_offset)).thickness(dot_size)

timeline_labels = [
    anim.scaling_text('0', timeline.p1, timeline_label_size),
    anim.scaling_text('1', timeline.p2, timeline_label_size),
]

def _find_nearest_left(points: _List[anim.point]) -> anim.point:
    lonely = runners_centers[lonely_runner_index()]
    lefts = [pt for pt in points if pt.x() < 0. and pt != lonely]
    if not lefts:
        return lonely
    nearest = min([(pt.distance_squared(lonely), pt) for pt in lefts])
    return nearest[1]

def _find_nearest_right(points: _List[anim.point]) -> anim.point:
    lonely = runners_centers[lonely_runner_index()]
    rights = [pt for pt in points if pt.x() > 0. and pt != lonely]
    if not rights:
        return lonely
    nearest = min([(pt.distance_squared(lonely), pt) for pt in rights])
    return nearest[1]

def _in_lonely_zone(point: anim.point) -> bool:
    lonely = runners_centers[lonely_runner_index()]
    angle = anim.four_points_angle(track_center, lonely, track_center, point)
    zone_size = lonely_zone_size()
    return -zone_size <= angle <= zone_size

class runner_colorizer:
    colorizing = False

    def __init__(self, runner):
        self.runner = runner
        runner.center.add_user(self)

    def _update_geometry(self):
        runner = self.runner
        center = runner.center
        if not runner_colorizer.colorizing:
            runner.fill(anim.white)
        elif center == runners_centers[lonely_runner_index()]:
            runner.fill(anim.blue)
        elif _in_lonely_zone(center):
            runner.fill(anim.red)
        elif center == _find_nearest_left(runners_centers):
            runner.fill(anim.green)
        elif center == _find_nearest_right(runners_centers):
            runner.fill(anim.green)
        else:
            runner.fill(anim.white)

runners_colorizers: _List[runner_colorizer] = []

def _gen_runners():
    global runners_centers
    global runners
    global runner_colorizers

    runners_centers = [anim.point(0., track_radius) for speed in runners_speeds()]
    runners = [anim.circle(center, dot_size).fill(anim.white) for center in runners_centers]
    runners_colorizers = [runner_colorizer(runner) for runner in runners]

def _gen_lonely_space():
    global lonely_space

    lonely = runners_centers[lonely_runner_index()]

    left  = anim.selected_point([runner for runner in runners_centers], _find_nearest_left )
    right = anim.selected_point([runner for runner in runners_centers], _find_nearest_right)

    lonely_space  = anim.partial_circle(track_center, lonely_radius, left, right).thickness(0.).outline(anim.no_color).fill(anim.green)
    lonely_space.setZValue(-1.)

def _gen_lonely_zone():
    global lonely_zone

    count = runners_count()
    if count > 2:
        zone_start = anim.create_relative_point_around_center(track_center, track_radius, anim.pi / 2 + lonely_zone_size())
        zone_end = anim.create_relative_point_around_center(track_center, track_radius, anim.pi / 2 + anim.tau - lonely_zone_size())
        lonely_zone  = anim.partial_circle(track_center, lonely_radius, zone_start, zone_end)
    else:
        lonely_zone  = anim.circle(track_center, lonely_radius)
    lonely_zone.thickness(0.).outline(anim.no_color).fill(anim.red)

def _order_items():
    for runner in runners:
        runner.setZValue(1.)
    lonely_zone.setZValue(-2.)
    lonely_space.setZValue(-3.)


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    _gen_runners()
    _gen_lonely_space()
    _gen_lonely_zone()
    _order_items()

    actors = [
        [anim.actor('Runner', '', rd) for rd in runners],
        anim.actor('Track', '', track),
        anim.actor('Label', '', track_label),
        [anim.actor('Label', '', label) for label in timeline_labels],
        anim.actor('Timeline', '', timeline),
        anim.actor('Lonely zone', '', lonely_zone),
        anim.actor('Lonely space', '', lonely_space),
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

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator) -> None:
    _reset_opacities()
    _reposition_points()
    _remove_zones(animation, scene)
    runner_colorizer.colorizing = False

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

        angles = [0.] + [i * anim.pi / 6.] * (count - i)
        animator.animate_value(angles, duration, anim.rotate_point_around(runner.center, track.center))
    animation.attach_pointing_arrow(runners[-1].center, scene)

def show_runners_running_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Runners

    Each one runs at their
    own speed. All speeds
    are different.
    '''
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., anim.tau * speed], duration, anim.rotate_point_around(runner.center, track.center))
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
        animator.animate_value([0., anim.tau * speed], duration, anim.rotate_point_around(runner.center, track.center))

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
    runner_colorizer.colorizing = True
    lonely = runners[lonely_runner_index()]
    animator.animate_value([anim.white, anim.blue], duration / 10., anim.change_fill_color(lonely))
    animator.animate_value([0., 1.], duration / 10., anim.reveal_item(lonely_zone))
    animator.animate_value([0., 1.], duration / 10., anim.reveal_item(lonely_space))
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., anim.tau * speed], duration, anim.rotate_point_around(runner.center, track.center))

def lonely_runner_unproven_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Unproven

    The lonely runner theorem
    is not proven...
    '''
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., anim.tau * speed], duration, anim.rotate_point_around(runner.center, track.center))

def lonely_runner_theorem_simplications_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Simplifications

    ... while unproven, some
    simplifications have been
    shown to be equivalent to
    the general theorem.
    '''
    for i, runner, speed in zip(range(runners_count()), runners, runners_speeds()):
        animator.animate_value([0., anim.tau * speed], duration, anim.rotate_point_around(runner.center, track.center))

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
        animator.animate_value([0., anim.tau * speed], duration, anim.rotate_point_around(runner.center, track.center))


#################################################################
#
# Animation

lonely_runner = anim.simple_animation.from_module(globals())
