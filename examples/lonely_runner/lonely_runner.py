import anim
from typing import List as _List
from .runners_allowed_intervals import *
from .runner import runner

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

def reset(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    animation.current_shot_index = -1


#################################################################
#
# Points and geometries

track_radius: float = 500.
track_center = anim.point(0., 0.)
runner_radius: float = 40.
timeline_thickness = 40.
track_width: float = runner_radius * 2.5
lonely_zone_radius: float = track_radius

track_label_size: float = 200.
lonely_zone_label_size: float = 100.
timeline_label_size: float = 80.

lonely_zone: anim.circle = None
half_lonely_zone: anim.circle = None
lonely_zone_label: anim.scaling_text = None

track = anim.circle(track_center, track_radius).thickness(track_width).outline(anim.sable)
track_label = anim.scaling_text('1', track_center, track_label_size)

timeline_offset: float = 300.

timeline = anim.line(
    anim.point( -track_radius, timeline_offset),
    anim.point( track_radius, timeline_offset)).thickness(timeline_thickness)

timeline_labels = [
    anim.scaling_text('0', timeline.p1, timeline_label_size),
    anim.scaling_text('1', timeline.p2, timeline_label_size),
]

def _gen_runners():
    runner.create_runners(runners_speeds(), lonely_runner_index(), runner_radius, track_radius)

def _gen_lonely_zone():
    global lonely_zone
    global half_lonely_zone

    count = runner.runners_count
    if count > 2:
        zone_start = anim.create_relative_point_around_center(track_center, track_radius, anim.pi / 2 + anim.tau * runner.lonely_zone_size)
        zone_end = anim.create_relative_point_around_center(track_center, track_radius, anim.pi / 2 + anim.tau - anim.tau * runner.lonely_zone_size)
        lonely_zone  = anim.partial_circle(track_center, lonely_zone_radius, zone_start, zone_end)
        half_lonely_zone  = anim.line(track_center, runner.lonely.center)
    else:
        lonely_zone  = anim.circle(track_center, lonely_zone_radius)
        track_top = anim.create_relative_point_around_center(track_center, track_radius, anim.hpi)
        half_lonely_zone  = anim.circle(track_top, lonely_zone_radius)
    lonely_zone.thickness(0.).outline(anim.no_color).fill(anim.pale_red)
    half_lonely_zone.thickness(5.).outline(anim.red)

    global lonely_zone_label

    lonely_zone_label = anim.scaling_text('1 / n', anim.point(anim.center_of(lonely_zone.get_all_points())), lonely_zone_label_size)

def _order_items():
    for r in runner.runners:
        r.setZValue(1.)
    runner.lonely.setZValue(2.)
    lonely_zone.setZValue(-2.)
    lonely_zone_label.setZValue(-1.)
    half_lonely_zone.setZValue(-2.)


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    _gen_runners()
    _gen_lonely_zone()
    _order_items()

    actors = [
        [anim.actor('Runner', '', r) for r in runner.runners],
        anim.actor('Track', '', track),
        anim.actor('Label', '', track_label),
        anim.actor('Label', '', lonely_zone_label),
        [anim.actor('Label', '', label) for label in timeline_labels],
        anim.actor('Timeline', '', timeline),
        anim.actor('Lonely zone', '', lonely_zone),
        anim.actor('Lonely zone', '', half_lonely_zone),
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
    for r in runner.runners:
        r.set_opacity(0.)

def _reposition_points() -> None:
    for pt in anim.find_all_of_type(globals(), anim.point):
        pt.reset()
    for circle in anim.find_all_of_type(globals(), anim.circle):
        circle.center.reset()
    for r in runner.runners:
        r.set_lap_fraction(0.)

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator) -> None:
    runner.colorizing = False
    _reset_opacities()
    _reposition_points()

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
    count = runner.runners_count
    for i, r in zip(range(count), runner.runners):
        opacities = [0.] + [0.] * i + [1.] * (count - i)
        animator.animate_value(opacities, duration, anim.reveal_item(r))

        lap_fractions = [0.] + [i  / 12.] * (count - i)
        animator.animate_value(lap_fractions, duration, r.anim_lap_fraction())
    animation.attach_pointing_arrow(runner.runners[-1].center, scene)

def show_runners_running_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Runners

    Each one runs at their
    own speed. All speeds
    are different.
    '''
    for r in runner.runnings:
        animator.animate_value([0., r.speed], duration, r.anim_lap_fraction())
    animation.attach_pointing_arrow(runner.runnings[0].center, scene)

def lonely_runner_theorem_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Lonely Runner Theorem

    The lonely runner theorem
    claims that each runner
    will eventually be lonely
    at some time.
    '''
    animator.animate_value([1., 0.], duration, anim.reveal_item(track_label))
    animation.anim_pointing_arrow([r.center for r in runner.runners], duration, scene, animator)

def lonely_runner_definition_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Lonely?

    A given runner is lonely
    if all other runners are
    far enough.
    
    For example, let's look
    at this runner.
    '''
    runner.colorizing = True
    animator.animate_value([anim.white, anim.blue], duration / 10., anim.change_fill_color(runner.lonely))
    radius = runner.lonely.radius
    animator.animate_value([radius, radius * 2, radius, radius * 2, radius, radius * 2, radius], duration, anim.change_radius(runner.lonely))
    animation.anim_pointing_arrow(runner.lonely.center, arrow_duration, scene, animator)

def lonely_runner_exclusion_zone_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Exclusion Zone

    This runner is lonely when
    other runners are outside
    this exclusion zone.
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(lonely_zone))
    animation.anim_pointing_arrow(anim.center_of(lonely_zone.get_all_points()), arrow_duration, scene, animator)

def lonely_runner_exclusion_sides_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Exclusion Zone

    The exclusion zone extends
    equally on each side of
    the lonely runner.
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(half_lonely_zone))
    animation.anim_pointing_arrow(anim.center_of(lonely_zone.get_all_points()), arrow_duration, scene, animator)

def lonely_runner_exclusion_distance_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Exclusion Distance

    The exclusion distance is
    set to 1 over the number
    of runners.

    (Recall, the track length
    is set to 1, too.)
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(lonely_zone_label))
    animation.anim_pointing_arrow(anim.center_of(lonely_zone.get_all_points()), arrow_duration, scene, animator)

def lonely_runner_far_enough_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Far Enough

    While runners lap around
    the track, they go in and
    out of the exclusion zone.
    '''
    runner.colorizing = True
    for r in runner.runnings:
        animator.animate_value([0., r.speed], duration, r.anim_lap_fraction())
    animation.anim_pointing_arrow(anim.center_of(lonely_zone.get_all_points()), arrow_duration, scene, animator)

def lonely_runner_unproven_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Unproven

    The lonely runner theorem
    is not proven...
    '''
    for r in runner.runnings:
        animator.animate_value([0., r.speed], duration, r.anim_lap_fraction())

def lonely_runner_theorem_simplications_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Simplifications

    ... while unproven, some
    simplifications have been
    shown to be equivalent to
    the general theorem.
    '''
    animator.animate_value([anim.white, anim.blue], duration / 10., anim.change_fill_color(runner.lonely))
    for r in runner.runnings:
        animator.animate_value([0., r.speed], duration, r.anim_lap_fraction())

def lonely_runner_theorem_speeds_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Integer speeds

    For example, the speeds
    can all be integers, they
    can all be positive and
    one speed can be set to
    zero.
    '''
    for r in runner.runnings:
        animator.animate_value([0., r.speed], duration, r.anim_lap_fraction())


#################################################################
#
# Animation

lonely_runner = anim.simple_animation.from_module(globals())
