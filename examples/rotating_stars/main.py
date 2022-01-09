import animation
import star
from qt_helpers import *
import anim

app = create_app()

current_star = star.star()
options = star.star_options()

timer_delay = 10
timer = create_timer(timer_delay)
timer.setSingleShot(False)
playing = False
scene = anim.scene()
animator = None

star_anim = animation.animation(current_star, options)
step_names = [] # list(map(lambda i: i[1][1], sorted(stepper.steps.items())))

control_dock, control_layout = create_dock("Play Controls")

step_name_list = create_list("Current Step", step_names, control_layout)
step_button = create_button("Step", control_layout)
play_button = create_button("Play", control_layout)
stop_button = create_button("Stop", control_layout)
reset_button = create_button("Reset", control_layout)
add_stretch(control_layout)

anim_dock, anim_layout = create_dock("Animation Controls")

delay_box = create_number_range_slider("Animation speed (ms)", 0, 100, timer_delay, anim_layout)
add_stretch(anim_layout)

star_dock, star_layout = create_dock("Star Type")

sides_box = create_number_range_slider("Number of branches", 2, 20, current_star.sides, star_layout)
skip_box = create_number_range_slider("Star branch skip", 1, 100, current_star.skip, star_layout)
radius_ratio_box = create_number_range_slider("Percent of radius", 0, 100, 90, star_layout)
add_stretch(star_layout)

draw_dock, draw_layout = create_dock("Draw")

draw_intra_option = create_option("Draw intra-circle polygons", draw_layout, options.draw_intra_circle_polygons)
draw_inter_option = create_option("Draw inter-circle polygons", draw_layout, options.draw_inter_circle_polygons)
draw_dots_option = create_option("Draw dots", draw_layout, options.draw_dots)
draw_inner_option = create_option("Draw inner circles", draw_layout, options.draw_inner_circles)
draw_outer_option = create_option("Draw outer circle", draw_layout, options.draw_outer_circle)
draw_star_option = create_option("Draw the star", draw_layout, options.draw_star)

window = create_main_window("Rotating Stars", scene.get_widget())
add_dock(window, control_dock)
add_dock(window, anim_dock)
add_dock(window, star_dock)
add_dock(window, draw_dock)


def advance_step():
    scene.reset()
    shots = star_anim.animate_all()
    anim.shot.play_all(shots, scene, animator)
    scene.ensure_all_contents_fit()

@reset_button.clicked.connect
def on_reset():
    #stepper.reset()
    pass

@step_button.clicked.connect
def on_step():
    advance_step()

@play_button.clicked.connect
def on_play():
    global playing
    playing = True
    timer.start()

@stop_button.clicked.connect
def on_stop():
    global playing
    playing = False
    timer.stop()

@delay_box.valueChanged.connect
def on_delay_changed(value):
    #animator.anim_duration = int(value)
    timer.setInterval(int(value))

@sides_box.valueChanged.connect
def on_sides_changed(value):
    try:
        new_sides = int(value)
    except:
        return
    global current_star
    current_star = star.star(new_sides, current_star.skip, current_star.inner_circle_dot_ratio)
    star_anim.star = current_star
    star_anim.reset()

@skip_box.valueChanged.connect
def on_skip_changed(value):
    try:
        new_skip = int(value)
    except:
        return
    global current_star
    current_star = star.star(current_star.sides, new_skip, current_star.inner_circle_dot_ratio)
    star_anim.star = current_star
    star_anim.reset()

@radius_ratio_box.valueChanged.connect
def on_radius_ratio_changed(value):
    try:
        new_value = float(value)
    except:
        return
    global current_star
    current_star = star.star(current_star.sides, current_star.skip, new_value / 100.)
    star_anim.star = current_star
    star_anim.reset()

@timer.timeout.connect
def on_timer():
    advance_step()

@draw_intra_option.stateChanged.connect
def on_draw_intra(state):
    options.draw_intra_circle_polygons = bool(state)

@draw_inter_option.stateChanged.connect
def on_draw_inter(state):
    options.draw_inter_circle_polygons = bool(state)

@draw_dots_option.stateChanged.connect
def on_draw_dots(state):
    options.draw_dots = bool(state)

@draw_inner_option.stateChanged.connect
def on_draw_inner(state):
    options.draw_inner_circles = bool(state)

@draw_outer_option.stateChanged.connect
def on_draw_outer(state):
    options.draw_outer_circle = bool(state)

@draw_star_option.stateChanged.connect
def on_draw_star(state):
    options.draw_star = bool(state)

start_app(app, window)

