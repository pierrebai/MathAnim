from anim.options import option
from ..animation import animation
from ..animator import animator
from ..scene import scene

from .ui import *
from .options_ui import create_options_ui
from .actors_ui import create_actors_ui
from .shots_ui import create_shots_ui

def create_app_window(animation: animation, scene: scene, animator: animator) -> QMainWindow:
    anim_dock, anim_layout = create_dock("Animation Controls")

    buttons_layout = create_horiz_container(anim_layout)
    play_button = create_button("Play", buttons_layout)
    step_button = create_button("Step", buttons_layout)
    stop_button = create_button("Stop", buttons_layout)
    reset_button = create_button("Reset", buttons_layout)
    current_time_box = create_number_slider("Current time", 0, 1000, 0, anim_layout)
    add_stretch(anim_layout)

    options_dock, _ = create_options_ui(scene, animation, animator)
    draw_dock, _ = create_actors_ui(animation)
    shots_dock, _ = create_shots_ui(animation)

    window = create_main_window(animation.name, scene.get_widget())
    add_dock(window, shots_dock)
    add_dock(window, anim_dock)
    add_dock(window, options_dock)
    add_dock(window, draw_dock)

    @play_button.clicked.connect
    def on_play():
        animation.play_all(scene, animator)

    @step_button.clicked.connect
    def on_step():
        if not animation.playing:
            animation.play_next_shot(scene, animator)

    @stop_button.clicked.connect
    def on_stop():
        animation.stop(scene, animator)

    @reset_button.clicked.connect
    def on_reset():
        was_playing = animation.playing
        animation.stop(scene, animator)
        animation.reset(scene, animator)
        if was_playing:
            animation.play_all(scene, animator)

    @current_time_box.valueChanged.connect
    def on_current_time_changed(value):
        animator.set_current_time_fraction(int(value) / 1000.)

    @animator.anim_group.current_time_changed.connect
    def on_anim_current_time_changed(value: float):
        current_time_box.setValue(int(round(1000 * value)))

    return window
