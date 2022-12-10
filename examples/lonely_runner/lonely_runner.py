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

class lonely_solver:
    def __init__(self):
        self.reset()

    def reset(self):
        self.normalized_running_runners = generate_running_runners(runners_speeds(), lonely_runner_index())
        self.allowed_time_intervals = [(0.0, 1.0)]
        self.next_runner_to_solve = 0

    def gen_runner_allowed_time_intervals(self, which: int) -> _List[_List[float]]:
        self.runner_allowed_time_intervals = generate_one_runner_allowed_time_intervals(self.normalized_running_runners[which], runner.runners_count)
        self.allowed_time_intervals = intersect_time_intervals(self.runner_allowed_time_intervals, self.allowed_time_intervals)
        return self.runner_allowed_time_intervals

    def get_next_runner_intervals_index(self) -> int:
        which = self.next_runner_to_solve
        self.next_runner_to_solve += 1
        return which

    def has_more_runner_intervals(self) -> bool:
        return self.next_runner_to_solve < len(self.normalized_running_runners)

solver: lonely_solver = None


#################################################################
#
# Points and geometries

class points:
    def __init__(self):
        self.runner_radius: float = 40.
        self.track_center = anim.point(0., 0.)
        self.track_radius: float = 500.
        self.track_width: float = self.runner_radius * 2.5

        self.timeline_thickness = 10.
        self.timeline_offset: float = 400.
        self.timeline_width: float = self.track_radius * 2.

        self.runner_graph_height:  float = self.timeline_offset * 2. / 3.
        self.overal_graph_height: float = self.timeline_offset * 1. / 2.

        self.lonely_zone_radius: float = self.track_radius
        self.half_zone_thickness = 10.

        self.track_label_size: float = 200.
        self.lonely_zone_label_size: float = 100.
        self.timeline_label_size: float = 80.

    def reset(self):
        for pt in anim.find_all_of_type(self.__dict__, anim.point):
            pt.reset()

pts: points = None

class geometries:
    def __init__(self, pts: points):
        self.lonely_zone: anim.circle = None
        self.half_lonely_zone: anim.circle = None
        self.lonely_zone_label: anim.scaling_text = None

        self.track = anim.circle(pts.track_center, pts.track_radius).thickness(pts.track_width).outline(anim.sable)
        self.track_label = anim.scaling_text('1', pts.track_center, pts.track_label_size)

        self._gen_runners(pts)
        self._gen_lonely_zone(pts)
        self._order_items()

    def reset(self):
        for item in anim.find_all_of_type(self.__dict__, anim.item):
            item.set_opacity(0.)
        for circle in anim.find_all_of_type(self.__dict__, anim.circle):
            circle.center.reset()

    def _gen_runners(self, pts):
        runner.create_runners(runners_speeds(), lonely_runner_index(), pts.runner_radius, pts.track_radius)

    def _gen_lonely_zone(self, pts):
        count = runner.runners_count
        if count > 2:
            zone_start = anim.relative_radial_point(runner.lonely.center, 0., -anim.tau * runner.lonely_zone_size)
            zone_end = anim.relative_radial_point(runner.lonely.center, 0.,    anim.tau * runner.lonely_zone_size)
            self.lonely_zone  = anim.partial_circle(pts.track_center, pts.lonely_zone_radius, zone_start, zone_end)
            self.half_lonely_zone  = anim.line(pts.track_center, runner.lonely.center)
        else:
            zone_end = anim.relative_radial_point(runner.lonely.center, 0., anim.pi)
            self.lonely_zone  = anim.circle(pts.track_center, pts.lonely_zone_radius)
            self.half_lonely_zone  = anim.line(zone_end, runner.lonely.center)
        self.lonely_zone.thickness(0.).outline(anim.no_color).fill(anim.pale_red)
        self.half_lonely_zone.thickness(pts.half_zone_thickness).outline(anim.red)

        lonely_zone_label_pos = anim.point(anim.center_of(self.lonely_zone.get_all_points()))
        self.lonely_zone_label = anim.scaling_text(f'1 / {count}', lonely_zone_label_pos, pts.lonely_zone_label_size)

    def _order_items(self):
        for i, r in enumerate(runner.runners):
            r.setZValue(i)
        runner.lonely.setZValue(2000.)
        self.lonely_zone.setZValue(-2.)
        self.lonely_zone_label.setZValue(-1.)
        self.half_lonely_zone.setZValue(-2.)

geo: geometries = None


#################################################################
#
# Geometries for timeline graph

class timeline_geometries:
    def __init__(self, pts: points, animation: anim.animation, scene: anim.scene):
        self.pts = pts
        self.animation = animation
        self.scene = scene

        self.last_runner_intervals_graphs: _List[anim.item] = []
        self.last_overal_intervals_graphs: _List[anim.item] = []
        self.next_to_last_overal_intervals_graphs: _List[anim.item] = []

        self.timeline = anim.line(
            anim.point(-pts.track_radius, pts.track_radius + pts.timeline_offset),
            anim.point( pts.track_radius, pts.track_radius + pts.timeline_offset)).thickness(pts.timeline_thickness)

        self.labels = [
            anim.scaling_text('0', self.timeline.p1, pts.timeline_label_size),
            anim.scaling_text('1', self.timeline.p2, pts.timeline_label_size),
        ]

        self.solution_label = anim.scaling_text('', self.timeline.p1, pts.timeline_label_size)

        self.timeline.setZValue(2.)
        self.solution_label.setZValue(3.)

    def animate_runner_intervals(self, runner_allowed_time_intervals: _List[_List[float]], animator: anim.animator):
        self._remove_graphs(self.last_runner_intervals_graphs)
        new_intervals_graphs = self._gen_intervals_graphs(runner_allowed_time_intervals, self.pts.runner_graph_height, animator)
        self.last_runner_intervals_graphs = new_intervals_graphs
        self.animation.anim_pointing_arrow([anim.center_of(g.get_all_points()) for g  in new_intervals_graphs], duration, self.scene, animator)
        
    def animator_overal_intervals(self, allowed_time_intervals: _List[_List[float]], animator: anim.animator):
        self._remove_graphs(self.next_to_last_overal_intervals_graphs)
        self.next_to_last_overal_intervals_graphs = self.last_overal_intervals_graphs[:]
        for graph in self.next_to_last_overal_intervals_graphs:
            graph.fill(anim.pale_green)
        new_intervals_graphs = self._gen_intervals_graphs(allowed_time_intervals, -self.pts.overal_graph_height, animator)
        self.last_overal_intervals_graphs = new_intervals_graphs

    def cleanup_final_intervals(self):
        self._remove_graphs(self.next_to_last_overal_intervals_graphs)
        self._remove_graphs(self.last_runner_intervals_graphs)

    def reset(self) -> None:
        try:
            self._remove_graphs(self.next_to_last_overal_intervals_graphs)
        except:
            pass
        try:
            self._remove_graphs(self.last_overal_intervals_graphs)
        except:
            pass
        try:
            self._remove_graphs(self.last_runner_intervals_graphs)
        except:
            pass

        self.last_runner_intervals_graphs = []
        self.last_overal_intervals_graphs = []
        self.next_to_last_overal_intervals_graphs = []
        for item in anim.find_all_of_type(self.__dict__, anim.item):
            item.set_opacity(0.)

    def _remove_graphs(self, graphs: _List):
        for graph in graphs:
            self.scene.remove_item(graph)
        self.scene.scene.invalidate(self.scene.scene.sceneRect())
        graphs.clear()

    def _gen_intervals_graphs(self, allowed_time_intervals: _List[_List[float]], height: float, animator: anim.animator):
        intervals_graphs = []
        for interval in allowed_time_intervals:
            graph = self._gen_interval_graph(interval, height, animator)
            intervals_graphs.append(graph)
        return intervals_graphs

    def _gen_interval_graph(self, interval: _List[float], height: float, animator: anim.animator):
        interval_width = interval[1] - interval[0]
        p1 = anim.two_points_convex_sum(self.timeline.p1, self.timeline.p2, interval[0])
        p2 = anim.relative_point(p1, anim.static_point(0., -height))
        if interval_width * self.pts.timeline_width > 1.0:
            allowed_graph = anim.create_two_points_rect(p1, p2)
        else:
            allowed_graph = anim.line(p1, p2)
        allowed_graph.outline(anim.no_color).thickness(0.).fill(anim.green).set_opacity(0.)
        self.scene.add_item(allowed_graph)

        animator.animate_value([0., 1.], duration / 4., anim.reveal_item(allowed_graph))

        graph_grow = [
            anim.static_point(0.             * self.pts.timeline_width, -height),
            anim.static_point(interval_width * self.pts.timeline_width, -height)]
        animator.animate_value(graph_grow, duration, anim.move_point(p2))

        return allowed_graph


timeline: timeline_geometries = None


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    global solver;   solver = lonely_solver()
    global pts;      pts = points()
    global geo;      geo = geometries(pts)
    global timeline; timeline = timeline_geometries(pts, animation, scene)

    actors = [
        [anim.actor('Runner', '', r) for r in runner.runners],
        [anim.actor('Label', '', r.label) for r in runner.runners],
        anim.actor('Track', '', geo.track),
        anim.actor('Label', '', geo.track_label),
        anim.actor('Label', '', geo.lonely_zone_label),
        [anim.actor('Label', '', label) for label in timeline.labels],
        anim.actor('Timeline', '', timeline.timeline),
        anim.actor('Lonely zone', '', geo.lonely_zone),
        anim.actor('Lonely zone', '', geo.half_lonely_zone),
        anim.actor('Solution', '', timeline.solution_label),
    ]
    animation.add_actors(actors, scene)
    rect_radius =  pts.track_radius + 50
    scene.add_item(anim.create_invisible_rect(-rect_radius, -rect_radius, rect_radius * 2, rect_radius * 4))


#################################################################
#
# Prepare animation

def _reset_runners() -> None:
    global next_runner_to_introduce
    next_runner_to_introduce = 0

    runner.always_colored = False
    for r in runner.runners:
        r.reset()
        r.set_opacity(0.)

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator) -> None:
    timeline.reset()
    geo.reset()
    pts.reset()
    _reset_runners()
    solver.reset()

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
    anim.anim_reveal_thickness(animator, duration / 4., geo.track)
    animation.anim_pointing_arrow(geo.track.get_circumference_point(-0.4), arrow_duration, scene, animator)

def measure_track_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Running track

    For simplicity, we will
    assume that the length
    of the track is one,
    in some arbitrary units.
    '''
    geo.track_label.center_on(geo.track)
    animator.animate_value([0., 1.], duration / 4., anim.reveal_item(geo.track_label))
    animation.anim_pointing_arrow(geo.track.get_circumference_point(-0.4), arrow_duration, scene, animator)

def introduce_runners_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Runners

    Many runners are making
    laps around the circular
    track.
    '''
    global next_runner_to_introduce
    count = runner.runners_count
    if next_runner_to_introduce < count:
        i = next_runner_to_introduce

        r = runner.runners[i]

        animator.animate_value([0., 1.], duration / (count * 3.), anim.reveal_item(r))
        anim.anim_ondulate_radius(animator, duration / count, r)

        animator.animate_value([(i-1) / 12., i  / 12.], duration / count, r.anim_lap_fraction())

        animation.attach_pointing_arrow(runner.runners[i].center, scene)

        next_runner_to_introduce += 1
        if next_runner_to_introduce < count:
            animation.add_next_shots(anim.anim_description._create_shot(introduce_runners_shot))

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
    animator.animate_value([1., 0.], duration, anim.reveal_item(geo.track_label))
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
    animator.animate_value([0., 1.], duration, anim.reveal_item(geo.lonely_zone))
    animation.anim_pointing_arrow(anim.center_of(geo.lonely_zone.get_all_points()), arrow_duration, scene, animator)

def exclusion_sides_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Exclusion Zone

    The exclusion zone extends
    equally on each side of
    the lonely runner.
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(geo.half_lonely_zone))
    animation.anim_pointing_arrow(anim.center_of(geo.lonely_zone.get_all_points()), arrow_duration, scene, animator)

def exclusion_distance_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Exclusion Distance

    The exclusion distance is
    set to 1 over the number
    of runners.
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(geo.lonely_zone_label))
    animation.anim_pointing_arrow(anim.center_of(geo.lonely_zone.get_all_points()), arrow_duration, scene, animator)

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
    animator.animate_value([1., 0.], duration / 10., anim.reveal_item(geo.half_lonely_zone))
    animator.animate_value([1., 0.], duration / 10., anim.reveal_item(geo.lonely_zone_label))
    for r in runner.runners:
        r.set_colored(True)
        animator.animate_value([0., r.speed], duration * 3., r.anim_lap_fraction())
    animation.anim_pointing_arrow(anim.center_of(geo.lonely_zone.get_all_points()), arrow_duration, scene, animator)

def introduce_timeline_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Timeline

    To see how we can solve
    the lonely runner theorem,
    we can draw on a timeline
    when each runner is in or
    out of the exclusion zone.
    '''
    animator.animate_value([0., 1.], duration, anim.reveal_item(timeline.timeline))
    for label in timeline.labels:
        animator.animate_value([0., 1.], duration, anim.reveal_item(label))
    animation.anim_pointing_arrow(anim.center_of(timeline.timeline.get_all_points()), arrow_duration, scene, animator)

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
    if solver.has_more_runner_intervals():
        which = solver.get_next_runner_intervals_index()
        timeline.animate_runner_intervals(solver.gen_runner_allowed_time_intervals(which), animator)
        r = runner.runnings[which]
        animator.animate_value([0., r.speed], duration, r.anim_lap_fraction())
        if runner.lonely.speed:
            animator.animate_value([0., runner.lonely.speed], duration, runner.lonely.anim_lap_fraction())

def overal_allowed_times_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Timeline

    The allowed time intervals
    of each runner is combined
    with previous intervals to
    produce the final allowed
    time intervals.
    '''
    if solver.has_more_runner_intervals():
        timeline.animator_overal_intervals(solver.allowed_time_intervals, animator)
        animation.anim_pointing_arrow(anim.center_of(timeline.last_overal_intervals_graphs[0].get_all_points()), arrow_duration, scene, animator)

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
    if solver.has_more_runner_intervals():
        which = solver.get_next_runner_intervals_index()
        timeline.animate_runner_intervals(solver.gen_runner_allowed_time_intervals(which), animator)
        timeline.animator_overal_intervals(solver.allowed_time_intervals, animator)
        r = runner.runnings[which]
        animator.animate_value([0., r.speed], duration, r.anim_lap_fraction())
        if runner.lonely.speed:
            animator.animate_value([0., runner.lonely.speed], duration, runner.lonely.anim_lap_fraction())
    if solver.has_more_runner_intervals():
        animation.add_next_shots(anim.anim_description._create_shot(all_runners_on_timeline_shot))

def final_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    The Final Solution

    One possible solution to
    the given problem, showing
    where each runner can be,
    outside the exclusion zone.

    They each arrive at their
    position at the shown time.
    '''
    timeline.cleanup_final_intervals()
    first_valid_time = (solver.allowed_time_intervals[0][0] + solver.allowed_time_intervals[0][1]) / 2.
    runner.always_colored = False
    for r in runner.runners:
        r.set_colored(True)
        animator.animate_value([0., first_valid_time * r.speed], duration * 2., r.anim_lap_fraction())

    if timeline.last_overal_intervals_graphs:
        animation.anim_pointing_arrow(anim.center_of(timeline.last_overal_intervals_graphs[0].get_all_points()), arrow_duration, scene, animator)
        timeline.solution_label.setText(f'{first_valid_time:3.3}')
        timeline.solution_label.position.set_absolute_point(max(timeline.last_overal_intervals_graphs[0].get_all_points(), key=lambda pt: pt.x() + pt.y()))
        animator.animate_value([0., 1.], duration, anim.reveal_item(timeline.solution_label))


#################################################################
#
# Animation

lonely_runner = anim.simple_animation.from_module(globals())
