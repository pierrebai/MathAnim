from .ui import create_dock, create_list, empty_dock, select_in_list, add_stretch
from ..animation import animation

from PySide6.QtWidgets import QDockWidget, QVBoxLayout

from typing import Tuple

def _fill_shots_ui(animation: animation, layout: QVBoxLayout) -> None:
    ui = create_list("Steps", [shot.name for shot in animation.shots], layout)
    
    def on_shot_changed(scene, animator, shot):
        select_in_list(shot.name, ui)
    signal_connection = animation.on_shot_changed.connect(on_shot_changed)

    def disconnect():
        animation.on_shot_changed.disconnect(signal_connection)
    ui.auto_disconnect = disconnect

    add_stretch(layout)

def create_shots_ui(animation: animation) -> Tuple[QDockWidget, QVBoxLayout]:
    """
    Creates the UI showning the list of animation steps (animation shots).
    """
    dock, layout = create_dock("Animation Steps")
    _fill_shots_ui(animation, layout)
    return dock, layout

def update_shots_ui(animation: animation, layout: QVBoxLayout) -> None:
    empty_dock(layout)
    _fill_shots_ui(animation, layout)
