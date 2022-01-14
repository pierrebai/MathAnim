from .ui import create_dock, create_list, select_in_list, add_stretch
from ..animation import animation

from PyQt5.QtWidgets import QDockWidget, QVBoxLayout

from typing import Tuple

def create_shots_ui(animation: animation) -> Tuple[QDockWidget, QVBoxLayout]:
    """
    Creates the UI showning the list of animation steps (animation shots).
    """
    dock, layout = create_dock("Animation Steps")
    ui = create_list("Steps", [shot.name for shot in animation.shots], layout)
    def on_shot_changed(scene, animator, shot):
        select_in_list(shot.name, ui)
    animation.on_shot_changed = on_shot_changed
    add_stretch(layout)
    return dock, layout
