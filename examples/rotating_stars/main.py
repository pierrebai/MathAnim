import animation
import anim

from PySide6.QtCore import Slot

app = anim.ui.create_app()

scene = anim.scene()
animator = anim.animator()
star_anim = animation.animation(scene)
scene.ensure_all_contents_fit()

anim_dock, anim_layout = anim.ui.create_dock("Animation Controls")

play_button = anim.ui.create_button("Play", anim_layout)
stop_button = anim.ui.create_button("Stop", anim_layout)
speed_box = anim.ui.create_number_range_slider("Animation speed", 1, 100, int(animator.anim_speedup * 20), anim_layout)
anim.ui.add_stretch(anim_layout)

options_dock, _ = anim.ui.create_options_ui(scene, star_anim, animator)
draw_dock, _ = anim.ui.create_actors_ui(star_anim)
shots_dock, _ = anim.ui.create_shots_ui(star_anim)

window = anim.ui.create_main_window("Rotating Stars", scene.get_widget())
anim.ui.add_dock(window, shots_dock)
anim.ui.add_dock(window, anim_dock)
anim.ui.add_dock(window, options_dock)
anim.ui.add_dock(window, draw_dock)

@play_button.clicked.connect
def on_play():
    star_anim.play(scene, animator)

@stop_button.clicked.connect
def on_stop():
    star_anim.stop(animator)

@speed_box.valueChanged.connect
def on_delay_changed(value):
    animator.anim_speedup = int(value) / 20.

def play_next_shot(shot: anim.shot, scene: anim.scene, animator: anim.animator):
    if star_anim.playing:
        star_anim.play_next_shot(scene, animator)

animator.shot_ended.connect(play_next_shot)

anim.ui.start_app(app, window)

