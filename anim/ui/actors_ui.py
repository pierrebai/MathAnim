from .ui import *
from ..animation import animation

from PySide6.QtWidgets import *

from typing import Tuple

def _connect_actor_ui(ui: QCheckBox, animation: animation, name) -> None:
    """
    Connects the check box changed signal to a function that updates
    the shown state of the anmation actors.
    """
    @ui.stateChanged.connect
    def on_changed(state):
        for actor in animation.actors:
            if actor.name == name:
                actor.show(bool(state))


def create_actors_ui(animation: animation) -> Tuple[QDockWidget, QVBoxLayout]:
    """
    Creates the UI to control which actors are shown.
    """
    dock, layout = create_dock("Draw Options")
    shown_by_names = animation.get_shown_actors_by_names()
    for name, shown in shown_by_names.items():
        ui = create_option(f"Draw {name}", layout, shown)
        # Note: connect must be out of the loop due to how variables
        #       are captured in inner functions.
        _connect_actor_ui(ui, animation, name)
    add_stretch(layout)
    return dock, layout
