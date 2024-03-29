from .ui import *

from ..animation import animation
from ..animator import animator
from ..scene import scene

from typing import Tuple

def _fill_animation_controls_ui(animation: animation, scene: scene, animator: animator, layout: QVBoxLayout) -> None:
    buttons_layout = create_horiz_container(layout)
    layout.play_button = create_button("Play", buttons_layout)
    add_button_shortcut(layout.play_button, QKeyCombination(Qt.ShiftModifier, Qt.Key_Space))
    layout.step_button = create_button("Step", buttons_layout)
    add_button_shortcut(layout.step_button, Qt.Key_Space)
    layout.stop_button = create_button("Stop", buttons_layout)
    add_button_shortcut(layout.stop_button, Qt.Key_Escape)
    layout.reset_button = create_button("Reset", buttons_layout)
    add_button_shortcut(layout.reset_button, Qt.Key_Backspace)
    layout.current_time_box = create_number_slider("Current time", 0, 1000, 0, layout)
    layout.animation_speed_box = create_number_slider("Speed", 1, 100, 20, layout)
    layout.zoom_box = create_number_slider("Zoom", 10, 200, 10, layout)
    add_stretch(layout)


def _connect_animation_controls_ui(animation: animation, scene: scene, animator: animator, layout: QVBoxLayout) -> None:
    def on_play():
        animation.play(scene, animator)
    connect_auto_signal(layout.play_button, layout.play_button.clicked, on_play)

    def on_step():
        animation.play_next_shot(scene, animator)
    connect_auto_signal(layout.step_button, layout.step_button.clicked, on_step)

    def on_stop():
        animation.stop(scene, animator)
    connect_auto_signal(layout.stop_button, layout.stop_button.clicked, on_stop)

    def on_reset():
        was_playing = animation.playing
        animation.stop(scene, animator)
        animation.reset(scene, animator)
        animation.current_shot_index = -1
        if was_playing:
            animation.play(scene, animator)
    connect_auto_signal(layout.reset_button, layout.reset_button.clicked, on_reset)

    def on_current_time_changed(value):
        animator.set_current_time_fraction(int(value) / 1000.)
    connect_auto_signal(layout.current_time_box, layout.current_time_box.valueChanged, on_current_time_changed)

    def on_anim_current_time_changed(value: float):
        layout.current_time_box.setValue(int(round(1000 * value)))
    connect_auto_signal(animator.anim_group, animator.anim_group.current_time_changed, on_anim_current_time_changed)

    def on_anim_speed_changed(value: float):
        animator.anim_speedup = float(value) / 20.
        animation.reset_play(scene, animator)
    connect_auto_signal(layout.animation_speed_box, layout.animation_speed_box.valueChanged, on_anim_speed_changed)

    def on_zoom_changed(value: float):
        scene.view.zoom = float(value) / 10.
        scene.view.fit_rectangle(scene.scene.sceneRect())
    connect_auto_signal(layout.zoom_box, layout.zoom_box.valueChanged, on_zoom_changed)


def _disconnect_animation_controls_ui(animation: animation, scene: scene, animator: animator, layout: QVBoxLayout) -> None:
    disconnect_auto_signals(layout.play_button)
    disconnect_auto_signals(layout.step_button)
    disconnect_auto_signals(layout.stop_button)
    disconnect_auto_signals(layout.reset_button)
    disconnect_auto_signals(layout.current_time_box)
    disconnect_auto_signals(layout.animation_speed_box)
    disconnect_auto_signals(layout.zoom_box)
    disconnect_auto_signals(animator.anim_group)


def create_animation_controls_ui(animation: animation, scene: scene, animator: animator) -> Tuple[QDockWidget, QVBoxLayout]:
    dock, layout = create_dock("Animation Controls")
    _fill_animation_controls_ui(animation, scene, animator, layout)
    _connect_animation_controls_ui(animation, scene, animator, layout)
    return dock, layout


def update_animation_controls_ui(animation: animation, scene: scene, animator: animator, dock: QDockWidget, layout: QVBoxLayout) -> QVBoxLayout:
    _disconnect_animation_controls_ui(animation, scene, animator, layout)
    _connect_animation_controls_ui(animation, scene, animator, layout)
    return layout
