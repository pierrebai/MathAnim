from typing import List as _List
from math import floor as _floor, ceil as _ceil

def generate_one_runner_allowed_time_intervals(
    runner : int, runners_count: int) -> _List[_List[float]]:
    '''
    Generate the time intervals when the runner is outside of the exclusion zone.

    The exclusion zone goes from [-1/n, 1/n], for n runners.
    
    (Note that we pass the list of runners exluding the immobile one, so that
    the length of the runners list is smaller than the runner count. That is
    why we pass the runner count explictly, for clarity. That avoids somewhat
    'mysteriously' adding one to the length of the array, which would make the
    code less clear.)

    In the time interval [0, 1], each runner will be in the exclusion zone 2/n
    of the time. How that time is distributed in the [0, 1] changes for each
    runner.

    A runner with speed r will run around the circle in time 1/r. These r laps
    produces r exclusion zones, each 2/(n*r) in size, all equidistant in
    the [0,1] interval.

    We see that r exclusions zones of size 2(n*r) does indeed produce a total
    coverage of 2/n.
    '''
    intervals = []
    time_for_cycle = 1. / runner
    time_for_away  = 1. / (runner * runners_count)
    time_for_back  = time_for_cycle - time_for_away
    for i in range(0, int(_ceil(runner))):
        cycle_time = i * time_for_cycle
        intervals.append((cycle_time + time_for_away, cycle_time + time_for_back))
    return intervals


def intersect_time_intervals(intervals_1: _List[_List[float]], intervals_2: _List[_List[float]]) -> _List[_List[float]]:
    '''
    Intersect two lists of time intervals, creating a new list of time intervals.
    '''
    intervals = []
    index_1 = 0
    index_2 = 0
    while index_1 < len(intervals_1) and index_2 < len(intervals_2):
        interval_1 = intervals_1[index_1]
        interval_2 = intervals_2[index_2]
        if interval_1[0] < interval_2[0]:
            if interval_1[1] < interval_2[0]:
                index_1 += 1
            else:
                if interval_1[1] < interval_2[1]:
                    intervals.append([interval_2[0], interval_1[1]])
                    index_1 += 1
                else:
                    intervals.append([interval_2[0], interval_2[1]])
                    index_2 += 1
        else:
            if interval_2[1] < interval_1[0]:
                index_2 += 1
            else:
                if interval_2[1] < interval_1[1]:
                    intervals.append([interval_1[0], interval_2[1]])
                    index_2 += 1
                else:
                    intervals.append([interval_1[0], interval_1[1]])
                    index_1 += 1
    return intervals


def generate_all_allowed_time_intervals(
    runners: _List[int], runners_count: int) -> float:
    '''
    Generate all time intervals where all runners are simultaneously outside
    of the exclusion zone.
    '''
    intervals = [(0.0, 1.0)]
    for r in runners:
        runner_intervals = generate_one_runner_allowed_time_intervals(r, runners_count)
        intervals = intersect_time_intervals(intervals, runner_intervals)
    return intervals


def generate_running_runners(runners: _List[int], lonely_runner_index: int):
    '''
    Generate the list of runners that will be running, removing the runner
    that will be lonely and immobile.

    All runners speed are adjusted to make that runner immobile and then
    are made all positive.

    The fact that any runner's speed can be set to zero is easy to see:
    imagine the track rotates counter to the direction of the runner you
    want to be stopped. The tract rotation can be set to the same speed
    as that runner. All runners relative speed stay the same, but now that
    runner is not moving.
    
    The reason all speed can be made positive is exploiting the two facts
    that the exclusion zone is symmetric around the lonely runner and that
    the circular track is also symmetric. So, if a runner would be outside
    the exclusion zone when running at a given speed in one direction, it
    would also be outside the zone when running in the other direction.
    This allows us to always only use positive speeds.
    '''
    if not runners:
        return []
    lonely_runner_speed = runners[lonely_runner_index]
    running_runners = [abs(speed - lonely_runner_speed) for speed in runners if speed != lonely_runner_speed]
    return running_runners


class runners_solution:
    '''
    Generate all time intervals where all runners are simultaneously outside
    of the exclusion zone. Explicitly keep the earliest solution time.
    
    Also contains, for each runner:
       - the total ran distance for.
       - the fractional distance ran around the circle of unit circumference.
       - The distance from zero.
       - The scaled distance from zero, where one equals the desired minimum
         distance from zero, which is equal to 1 over the number of runners,
         including the immobile one.
    '''
    def __init__(self, runners: _List[int], lonely_runner_index: int) -> None:
        self.runners = runners
        self.lonely_runner_index = lonely_runner_index
        running_runners = generate_running_runners(runners, lonely_runner_index)
        runners_count = len(runners)
        self.intervals = generate_all_allowed_time_intervals(running_runners, runners_count)
        self.generate_stats()

    def generate_stats(self):
        self.earliest_solution_time = self.intervals[0][0] if self.intervals else 0.
        self.ran_distances = [r * self.earliest_solution_time for r in self.runners]
        self.fractional_distances = [r_d - _floor(r_d) for r_d in self.ran_distances]

        lrd = self.fractional_distances[self.lonely_runner_index]
        runners_count = len(self.runners)

        self.distances_from_lonely = [min(abs(f_d - lrd), abs(1. - (f_d - lrd))) for f_d in self.fractional_distances]
        self.scaled_distances_from_lonely = [f_z * runners_count for f_z in self.distances_from_lonely]

    def __str__(self):
        '''
        Print a time where all runners are simultaneously outside the exclusion zone.
        There are always more than one time, we simply return the earliest one.
        '''
        last_printed_interval = 4 if len(self.intervals) > 4 else len(self.intervals)
        s = [
            f'{len(self.runners)} runners produced {len(self.intervals)} intervals: {self.intervals[0:last_printed_interval]}',
            f'At time {self.earliest_solution_time}...'
        ]

        lrs = self.runners[self.lonely_runner_index]
        head = '        Runner speed    Ran distance    Distance to Lonely    Ratio to minimum distance'
        s.append(head)
        for r, r_d, f_z, s_d_f_z in zip(self.runners, self.ran_distances, self.distances_from_lonely, self.scaled_distances_from_lonely):
            body = f' {"lonely" if r == lrs else "      "}  {r:6}      {r_d:12.3f}     {f_z:12.3f}       {s_d_f_z:12.1f}'
            s.append(body)
        return '\n'.join(s)


if __name__ == "__main__":
    #print(runners_solution([ 0, 1 ], 0))
    #print(runners_solution([ 0, 1, 2 ], 0))
    #print(runners_solution([ 0., 1.1, 3.2, 7.3 ], 0))
    #print(runners_solution([ 0, 1, 3, 4, 7 ], 0))
    print(runners_solution([ 0, 1, 3, 4, 7, 12 ], 0))
    #print(runners_solution([ 0, 1, 3, 4, 5, 9 ], 0))
    #print(runners_solution([ 0, 1, 4, 5, 6, 7, 11, 13 ], 0))
    #print(runners_solution([ 0, 1, 2, 3, 4, 5, 7, 12 ], 0))
    #print(runners_solution([ 4, 5, -7, 12, 0, 1, -2, 3,  ], 4))
    #print(runners_solution([ 4, 5, -7, 12, 0, 1, -2, 3,  ], 3))
    #print(runners_solution(list(range(0, 50000, 3000), 0)))
