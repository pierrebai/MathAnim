from .ui import *
from ..animation import animation

from PySide6.QtWidgets import *

from typing import Tuple

def _create_actor_ui(animation: animation, name: str, shown: bool, layout: QVBoxLayout) -> None:
    """
    Connects the check box changed signal to a function that updates
    the shown state of the anmation actors.
    """
    ui = create_checkbox(f"Draw {name}", layout, shown)
    def on_changed(state):
        for actor in animation.actors:
            if actor.name == name:
                actor.show(bool(state))
    connect_auto_signal(ui, ui.stateChanged, on_changed)

def _fill_actors_ui(animation: animation, layout: QVBoxLayout) -> None:
    shown_by_names = animation.get_shown_actors_by_names()
    for name, shown in shown_by_names.items():
        # Note: connect must be out of the loop due to how variables
        #       are captured in inner functions.
        _create_actor_ui(animation, name, shown, layout)
    add_stretch(layout)

def create_actors_ui(animation: animation) -> Tuple[QDockWidget, QVBoxLayout]:
    """
    Creates the UI to control which actors are shown.
    """
    dock, layout = create_dock("Draw Options")
    _fill_actors_ui(animation, layout)
    return dock, layout

def update_actors_ui(animation, dock: QDockWidget, layout: QVBoxLayout) -> QVBoxLayout:
    layout = empty_dock(dock, layout)
    _fill_actors_ui(animation, layout)
    return layout
