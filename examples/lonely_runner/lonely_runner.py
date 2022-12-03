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

def runners_speeds() -> _List[float]:
    try:
        return [float(s) for s in runners_speeds_options.value.split()]
    except ValueError:
        return [0]

def lonely_runner_index() -> int:
    return min(int(lonely_runner_options.value), len(runners_speeds()))

def reset(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    animation.current_shot_index = -1


#################################################################
#
# Lonely runner solver

normalized_running_runners: _List[float] = []
allowed_time_intervals: _List[_List[float]] = [(0.0, 1.0)]
next_runner_to_solve: int = 0

def _gen_normalized_runners():
    global normalized_running_runners
  
    normalized_running_runners = generate_running_runners(runners_speeds(), lonely_runner_index())

    global allowed_time_intervals
    allowed_time_intervals = [(0.0, 1.0)]

    global next_runner_to_solve
    next_runner_to_solve = 0

def _gen_runner_allowed_time_intervals(which: int) -> _List[_List[float]]:
    global allowed_time_intervals
    global normalized_running_runners
    runner_allowed_time_intervals = generate_one_runner_allowed_time_intervals(normalized_running_runners[which], runner.runners_count)
    allowed_time_intervals = intersect_time_intervals(runner_allowed_time_intervals, allowed_time_intervals)
    return runner_allowed_time_intervals

def _get_next_runner_intervals_index() -> int:
    global next_runner_to_solve
    which = next_runner_to_solve
    next_runner_to_solve += 1
    return which

def _has_more_runner_intervals() -> bool:
    return next_runner_to_solve < len(normalized_running_runners)


#################################################################
#
# Points and geometries

runner_radius: float = 40.

track_center = anim.point(0., 0.)
track_radius: float = 500.
track_width: float = runner_radius * 2.5

timeline_thickness = 10.
timeline_offset: float = 400.
timeline_width: float = track_radius * 2.

runner_graph_height:  float = timeline_offset * 2. / 3.
overal_graph_height: float = timeline_offset * 1. / 2.

lonely_zone_radius: float = track_radius
half_zone_thickness = 10.

track_label_size: float = 200.
lonely_zone_label_size: float = 100.
timeline_label_size: float = 80.

lonely_zone: anim.circle = None
half_lonely_zone: anim.circle = None
lonely_zone_label: anim.scaling_text = None

track = anim.circle(track_center, track_radius).thickness(track_width).outline(anim.sable)
track_label = anim.scaling_text('1', track_center, track_label_size)

timeline = anim.line(
    anim.point(-track_radius, track_radius + timeline_offset),
    anim.point( track_radius, track_radius + timeline_offset)).thickness(timeline_thickness)

timeline_labels = [
    anim.scaling_text('0', timeline.p1, timeline_label_size),
    anim.scaling_text('1', timeline.p2, timeline_label_size),
]

timeline_solution_label = anim.scaling_text('', timeline.p1, timeline_label_size)

def _gen_runners():
    runner.create_runners(runners_speeds(), lonely_runner_index(), runner_radius, track_radius)

def _gen_lonely_zone():
    global lonely_zone
    global half_lonely_zone

    count = runner.runners_count
    if count > 2:
        zone_start = anim.relative_radial_point(runner.lonely.center, 0., anim.tau * runner.lonely_zone_size)
        zone_end = anim.relative_radial_point(runner.lonely.center, 0.,  -anim.tau * runner.lonely_zone_size)
        lonely_zone  = anim.partial_circle(track_center, lonely_zone_radius, zone_start, zone_end)
        half_lonely_zone  = anim.line(track_center, runner.lonely.center)
    else:
        lonely_zone  = anim.circle(track_center, lonely_zone_radius)
        zone_end = anim.relative_radial_point(runner.lonely.center, 0., anim.pi)
        half_lonely_zone  = anim.line(zone_end, runner.lonely.center)
    lonely_zone.thickness(0.).outline(anim.no_color).fill(anim.pale_red)
    half_lonely_zone.thickness(half_zone_thickness).outline(anim.red)

    global lonely_zone_label

    lonely_zone_label = anim.scaling_text(f'1 / {count}', anim.point(anim.center_of(lonely_zone.get_all_points())), lonely_zone_label_size)

def _order_items():
    for i, r in enumerate(runner.runners):
        r.setZValue(i * 3. + 1.)
        r.label.setZValue(i * 3. + 2.)
    runner.lonely.setZValue(2000.)
    runner.lonely.label.setZValue(2001.)
    lonely_zone.setZValue(-2.)
    lonely_zone_label.setZValue(-1.)
    half_lonely_zone.setZValue(-2.)
    timeline.setZValue(2.)
    timeline_solution_label.setZValue(3.)


#################################################################
#
# Geometries for timeline graph

last_runner_intervals_graphs: _List[anim.item] = []
last_overal_intervals_graphs: _List[anim.item] = []
next_to_last_overal_intervals_graphs: _List[anim.item] = []

def _remove_intervals_graphs(graphs: _List, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    for graph in graphs:
        scene.remove_item(graph)
    scene.scene.invalidate(scene.scene.sceneRect())
    graphs.clear()

def _gen_interval_graph(interval: _List[float], height: float, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    interval_width = interval[1] - interval[0]
    p1 = anim.two_points_convex_sum(timeline.p1, timeline.p2, interval[0])
    p2 = anim.relative_point(p1, anim.static_point(0., -height))
    if interval_width * timeline_width > 1.0:
        allowed_graph = anim.create_two_points_rect(p1, p2)
    else:
        allowed_graph = anim.line(p1, p2)
    allowed_graph.outline(anim.no_color).thickness(0.).fill(anim.green).set_opacity(0.)
    scene.add_item(allowed_graph)

    animator.animate_value([0., 1.], duration / 4., anim.reveal_item(allowed_graph))

    graph_grow = [
        anim.static_point(0.             * timeline_width, -height),
        anim.static_point(interval_width * timeline_width, -height)]
    animator.animate_value(graph_grow, duration, anim.move_point(p2))

    return allowed_graph

def _gen_intervals_graphs(allowed_time_intervals: _List[_List[float]], height: float, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    intervals_graphs = []
    for interval in allowed_time_intervals:
        graph = _gen_interval_graph(interval, height, animation, scene, animator)
        intervals_graphs.append(graph)
    return intervals_graphs

def _gen_runner_intervals_graph(runner_allowed_time_intervals: _List[_List[float]], animation: anim.animation, scene: anim.scene, animator: anim.animator):
    global last_runner_intervals_graphs
    _remove_intervals_graphs(last_runner_intervals_graphs, animation, scene, animator)
    new_intervals_graphs = _gen_intervals_graphs(runner_allowed_time_intervals, runner_graph_height, animation, scene, animator)
    arrow_anim_values = new_intervals_graphs if len(new_intervals_graphs) < 10 else new_intervals_graphs[:5] + new_intervals_graphs[-5:]
    animation.anim_pointing_arrow([anim.center_of(g.get_all_points()) for g  in new_intervals_graphs], duration, scene, animator)
    last_runner_intervals_graphs = new_intervals_graphs

def _merge_runner_intervals_with_overal_intervals(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    global last_overal_intervals_graphs
    global next_to_last_overal_intervals_graphs
    _remove_intervals_graphs(next_to_last_overal_intervals_graphs, animation, scene, animator)
    next_to_last_overal_intervals_graphs = last_overal_intervals_graphs[:]
    for graph in next_to_last_overal_intervals_graphs:
        graph.fill(anim.pale_green)
    new_intervals_graphs = _gen_intervals_graphs(allowed_time_intervals, -overal_graph_height, animation, scene, animator)
    last_overal_intervals_graphs = new_intervals_graphs


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    _gen_runners()
    _gen_normalized_runners()
    _gen_lonely_zone()
    _order_items()

    actors = [
        [anim.actor('Runner', '', r) for r in runner.runners],
        [anim.actor('Label', '', r.label) for r in runner.runners],
        anim.actor('Track', '', track),
        anim.actor('Label', '', track_label),
        anim.actor('Label', '', lonely_zone_label),
        [anim.actor('Label', '', label) for label in timeline_labels],
        anim.actor('Timeline', '', timeline),
        anim.actor('Lonely zone', '', lonely_zone),
        anim.actor('Lonely zone', '', half_lonely_zone),
        anim.actor('Solution', '', timeline_solution_label),
    ]
    animation.add_actors(actors, scene)
    rect_radius =  track_radius + 50
    scene.add_item(anim.create_invisible_rect(-rect_radius, -rect_radius, rect_radius * 2, rect_radius * 4))


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

def _reset_runners() -> None:
    runner.always_colored = False
    for r in runner.runners:
        r.reset()
        r.set_opacity(0.)

def _reset_timeline() -> None:
    global last_runner_intervals_graphs
    last_runner_intervals_graphs = []
    global last_overal_intervals_graphs
    last_overal_intervals_graphs = []
    global next_to_last_overal_intervals_graphs
    next_to_last_overal_intervals_graphs = []

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator) -> None:
    _reset_timeline()
    _reset_opacities()
    _reposition_points()
    _reset_runners()
    _gen_normalized_runners()

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
    for r in runner.runners:
        animator.animate_value([0., r.speed], duration * 3., r.anim_lap_fraction())
    if runner.runnings:
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
    runner.lonely.set_colored(True)
    animator.animate_value([anim.white, anim.blue], duration / 10., anim.change_fill_color(runner.lonely))
    radius = runner.lonely.radius
    animator.animate_value([radius, radius * 2, radius, radius * 2, radius, radius * 2, radius], duration, anim.change_radius(runner.lonely))
    animation.anim_pointing_arrow(runner.lonely.center, arrow_duration, scene, animator)

def exclusion_zone_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Exclusion Zone

    This runner is lonely when
    other runners are outside
    this exclusion zone.
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(lonely_zone))
    animation.anim_pointing_arrow(anim.center_of(lonely_zone.get_all_points()), arrow_duration, scene, animator)

def exclusion_sides_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Exclusion Zone

    The exclusion zone extends
    equally on each side of
    the lonely runner.
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(half_lonely_zone))
    animation.anim_pointing_arrow(anim.center_of(lonely_zone.get_all_points()), arrow_duration, scene, animator)

def exclusion_distance_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Exclusion Distance

    The exclusion distance is
    set to 1 over the number
    of runners.
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(lonely_zone_label))
    animation.anim_pointing_arrow(anim.center_of(lonely_zone.get_all_points()), arrow_duration, scene, animator)

def in_lonely_zone_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Runners Colors

    Runners in the exclusion
    zone are red.
    '''
    if runner.runners_count > 1:
        r = runner.runnings[-1]
        r.set_colored(False)
        r.fill(anim.red)
        animator.animate_value([0., runner.lonely_zone_size / 2.], duration, r.anim_lap_fraction())
        animation.attach_pointing_arrow(r.center, scene)

def barely_out_of_onely_zone_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Runners Colors

    Runners just out of the
    zone on either side are
    yellow.
    '''
    if runner.runners_count > 2:
        r = runner.runnings[-2]
        r.set_colored(False)
        r.fill(anim.red)
        animator.animate_value([runner.lonely_zone_size * 1. / 2., runner.lonely_zone_size], duration, r.anim_lap_fraction())
        animator.animate_value([anim.red, anim.yellow], duration, anim.change_fill_color(r))
        animation.attach_pointing_arrow(r.center, scene)

def completely_out_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Runners Colors

    Runners farther outside
    of the zone are green.
    '''
    if runner.runners_count > 3:
        r = runner.runnings[-3]
        r.set_colored(False)
        r.fill(anim.green)
        animator.animate_value([runner.lonely_zone_size, 0.5], duration, r.anim_lap_fraction())
        animation.attach_pointing_arrow(r.center, scene)

def far_enough_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Runners Colors

    While runners lap around
    the track, they go in and
    out of the exclusion zone.
    '''
    animator.animate_value([1., 0.], duration / 10., anim.reveal_item(half_lonely_zone))
    animator.animate_value([1., 0.], duration / 10., anim.reveal_item(lonely_zone_label))
    for r in runner.runners:
        r.set_colored(True)
        animator.animate_value([0., r.speed], duration * 3., r.anim_lap_fraction())
    animation.anim_pointing_arrow(anim.center_of(lonely_zone.get_all_points()), arrow_duration, scene, animator)

def introduce_timeline_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Timeline

    To see how we can solve
    the lonely runner theorem,
    we can draw on a timeline
    when each runner is in or
    out of the exclusion zone.
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(timeline))
    for label in timeline_labels:
        animator.animate_value([0., 1.], duration, anim.reveal_item(label))
    animation.anim_pointing_arrow(anim.center_of(timeline.get_all_points()), arrow_duration, scene, animator)

def first_runner_on_timeline_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Timeline

    To see how we can solve
    the lonely runner theorem,
    we can draw on a timeline
    when each runner is in or
    out of the exclusion zone.
    '''
    runner.always_colored = True
    if _has_more_runner_intervals():
        which = _get_next_runner_intervals_index()
        _gen_runner_intervals_graph(_gen_runner_allowed_time_intervals(which), animation, scene, animator)
        r = runner.runnings[which]
        animator.animate_value([0., r.speed], duration, r.anim_lap_fraction())

def overal_allowed_times_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Timeline

    The allowed time intervals
    of each runner is combined
    with previous intervals to
    produce the final allowed
    time intervals.
    '''
    if _has_more_runner_intervals():
        _merge_runner_intervals_with_overal_intervals(animation, scene, animator)
        animation.anim_pointing_arrow(anim.center_of(last_overal_intervals_graphs[0].get_all_points()), arrow_duration, scene, animator)

def all_runners_on_timeline_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Timeline

    As each other ruuners is
    added to the timeline, the
    allowed time interval are
    merged together.

    Each additional runner
    adds further restrictions
    until we are left with the
    final solution.
    '''
    if _has_more_runner_intervals():
        which = _get_next_runner_intervals_index()
        _gen_runner_intervals_graph(_gen_runner_allowed_time_intervals(which), animation, scene, animator)
        _merge_runner_intervals_with_overal_intervals(animation, scene, animator)
        r = runner.runnings[which]
        animator.animate_value([0., r.speed], duration, r.anim_lap_fraction())
    if _has_more_runner_intervals():
        animation.add_shots(anim.anim_description._create_shot(all_runners_on_timeline_shot))
    else:
        animation.add_shots(anim.anim_description._create_shot(final_shot_protype))

def final_shot_protype(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    The Final Solution

    One possible solution to
    the given problem, showing
    where each runner can be,
    outside the exclusion zone.

    They each arrive at their
    position at the shown time.
    '''
    _remove_intervals_graphs(next_to_last_overal_intervals_graphs, animation, scene, animator)
    _remove_intervals_graphs(last_runner_intervals_graphs, animation, scene, animator)
    first_valid_time = (allowed_time_intervals[0][0] + allowed_time_intervals[0][1]) / 2.
    runner.always_colored = False
    for r in runner.runners:
        r.set_colored(True)
        animator.animate_value([0., first_valid_time * r.speed], duration * 2., r.anim_lap_fraction())

    if last_overal_intervals_graphs:
        animation.anim_pointing_arrow(anim.center_of(last_overal_intervals_graphs[0].get_all_points()), arrow_duration, scene, animator)
        timeline_solution_label.setText(f'{first_valid_time:3.3}')
        timeline_solution_label.position.set_absolute_point(max(last_overal_intervals_graphs[0].get_all_points(), key=lambda pt: pt.x() + pt.y()))
        animator.animate_value([0., 1.], duration, anim.reveal_item(timeline_solution_label))


#################################################################
#
# Animation

lonely_runner = anim.simple_animation.from_module(globals())