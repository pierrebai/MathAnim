import animation
import anim

app = anim.ui.create_app()

anim_speed = 20
playing = False

def set_anim_speed(speed: int):
    global anim_speed
    anim_speed = speed
    animator.anim_duration = get_animation_duration()
    if playing:
        animator.stop()
        anim.shot.play_all(star_anim.shots, scene, animator)
        scene.ensure_all_contents_fit()


def get_animation_duration():
    return max(1000, (100 - anim_speed) * 1000)

scene = anim.scene()
animator = anim.animator(get_animation_duration())
star_anim = animation.animation(scene)

anim_dock, anim_layout = anim.ui.create_dock("Animation Controls")

play_button = anim.ui.create_button("Play", anim_layout)
stop_button = anim.ui.create_button("Stop", anim_layout)
speed_box = anim.ui.create_number_range_slider("Animation speed", 1, 100, anim_speed, anim_layout)
anim.ui.add_stretch(anim_layout)

options_dock, _ = anim.ui.create_options_ui(scene, star_anim, animator)
draw_dock, _ = anim.ui.create_actors_ui(star_anim)

window = anim.ui.create_main_window("Rotating Stars", scene.get_widget())
anim.ui.add_dock(window, anim_dock)
anim.ui.add_dock(window, options_dock)
anim.ui.add_dock(window, draw_dock)

def advance_step():
    global playing
    if playing:
        anim.shot.play_all(star_anim.shots, scene, animator)
        scene.ensure_all_contents_fit()

@play_button.clicked.connect
def on_play():
    global playing
    if not playing:
        playing = True
        advance_step()

@stop_button.clicked.connect
def on_stop():
    global playing
    playing = False
    animator.stop()

@speed_box.valueChanged.connect
def on_delay_changed(value):
    set_anim_speed(int(value))

animator.anim_done_callback = advance_step

anim.ui.start_app(app, window)

