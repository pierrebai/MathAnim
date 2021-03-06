from .ui import create_dock, create_named_list, empty_dock, select_in_list, add_stretch, connect_auto_signal
from ..animation import animation

from PySide6.QtWidgets import QDockWidget, QVBoxLayout

from typing import Tuple

def _fill_shots_ui(animation: animation, layout: QVBoxLayout) -> None:
    ui = create_named_list("Steps", animation.shots, layout, False)
    
    def on_shot_changed(scene, animator, shot):
        select_in_list(shot.name, ui)
    connect_auto_signal(animation, animation.on_shot_changed, on_shot_changed)

    add_stretch(layout)

def create_shots_ui(animation: animation) -> Tuple[QDockWidget, QVBoxLayout]:
    """
    Creates the UI showning the list of animation steps (animation shots).
    """
    dock, layout = create_dock("Animation Steps")
    _fill_shots_ui(animation, layout)
    return dock, layout

def update_shots_ui(animation: animation, dock: QDockWidget, layout: QVBoxLayout) -> QVBoxLayout:
    layout = empty_dock(dock, layout)
    _fill_shots_ui(animation, layout)
    return layout
