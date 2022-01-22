from .ui import *

from ..animation import animation
from ..animator import animator
from ..scene import scene

from typing import Tuple

def _fill_animation_controls_ui(animation: animation, scene: scene, animator: animator, layout: QVBoxLayout) -> None:
    buttons_layout = create_horiz_container(layout)
    play_button = create_button("Play", buttons_layout)
    step_button = create_button("Step", buttons_layout)
    stop_button = create_button("Stop", buttons_layout)
    reset_button = create_button("Reset", buttons_layout)
    current_time_box = create_number_slider("Current time", 0, 1000, 0, layout)
    add_stretch(layout)

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

def create_animation_controls_ui(animation: animation, scene: scene, animator: animator) -> Tuple[QDockWidget, QVBoxLayout]:
    dock, layout = create_dock("Animation Controls")
    _fill_animation_controls_ui(animation, scene, animator, layout)
    return dock, layout

def update_animation_controls_ui(animation: animation, scene: scene, animator: animator, dock: QDockWidget, layout: QVBoxLayout) -> QVBoxLayout:
    layout = empty_dock(dock, layout)
    _fill_animation_controls_ui(animation, scene, animator, layout)
    return layout
