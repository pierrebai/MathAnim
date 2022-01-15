from ..animation import animation
from ..animator import animator
from ..scene import scene

from .ui import *
from .options_ui import create_options_ui
from .actors_ui import create_actors_ui
from .shots_ui import create_shots_ui

def create_app_window(animation: animation, scene: scene, animator: animator) -> QMainWindow:
    anim_dock, anim_layout = create_dock("Animation Controls")

    play_button = create_button("Play", anim_layout)
    stop_button = create_button("Stop", anim_layout)
    reset_button = create_button("Reset", anim_layout)
    speed_box = create_number_range_slider("Animation speed", 1, 100, int(animator.anim_speedup * 20), anim_layout)
    add_stretch(anim_layout)

    options_dock, _ = create_options_ui(scene, animation, animator)
    draw_dock, _ = create_actors_ui(animation)
    shots_dock, _ = create_shots_ui(animation)

    window = create_main_window("Rotating Stars", scene.get_widget())
    add_dock(window, shots_dock)
    add_dock(window, anim_dock)
    add_dock(window, options_dock)
    add_dock(window, draw_dock)

    @play_button.clicked.connect
    def on_play():
        animation.play_all(scene, animator)

    @stop_button.clicked.connect
    def on_stop():
        animation.stop(animator)

    @reset_button.clicked.connect
    def on_reset():
        was_playing = animation.playing
        animation.stop(animator)
        animation.reset(scene)
        if was_playing:
            animation.play_all(scene, animator)

    @speed_box.valueChanged.connect
    def on_delay_changed(value):
        animator.anim_speedup = int(value) / 20.

    return window
