import animation
import anim

app = anim.ui.create_app()

anim_speed = 20
current_shot = -1
playing = False

scene = anim.scene()
animator = anim.animator()
star_anim = animation.animation(scene)
scene.ensure_all_contents_fit()

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

def play_next_shot():
    global playing
    if playing:
        global current_shot
        current_shot = (current_shot + 1) % len(star_anim.shots)
        shot = star_anim.shots[current_shot]
        shot.play(scene, animator)
        scene.ensure_all_contents_fit()
        animator.play()

@play_button.clicked.connect
def on_play():
    global playing
    if not playing:
        playing = True
        global current_shot
        current_shot = -1
        play_next_shot()

@stop_button.clicked.connect
def on_stop():
    global playing
    playing = False
    animator.stop()

@speed_box.valueChanged.connect
def on_delay_changed(value):
    global anim_speed
    anim_speed = int(value)
    animator.anim_speedup = anim_speed / 20.


animator.anim_done_callback = play_next_shot

anim.ui.start_app(app, window)

