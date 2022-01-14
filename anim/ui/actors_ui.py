from .ui import *
from ..actor import actor
from ..animation import animation

from PyQt5.QtWidgets import *

from typing import Tuple, Dict, List
from collections import defaultdict

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

def _get_actors_by_names(animation: animation) -> Dict[str, List[actor]]:
    """
    Returns a dict of actor lists indexed by the actor name.
    """
    actors_by_names = defaultdict(list)
    for actor in animation.actors:
        actors_by_names[actor.name].append(actor)
    return actors_by_names

def get_shown_actors_by_names(animation: animation) -> Dict[str, bool]:
    """
    Returns a dict of shown / not shown flags indexed by actor names.
    """
    return {
        name: actors[0].shown for name, actors in _get_actors_by_names(animation).items()
    }

def apply_shown_to_actors(animation: animation, shown_by_names: Dict[str, bool]) -> None:
    """
    Applies a preserved shown actors dictionary on the given animation actors.
    """
    for actor in animation.actors:
        if actor.name in shown_by_names:
            actor.show(shown_by_names[actor.name])

def create_actors_ui(animation: animation) -> Tuple[QDockWidget, QVBoxLayout]:
    """
    Creates the UI to control which actors are shown.
    """
    dock, layout = create_dock("Draw Options")
    shown_by_names = get_shown_actors_by_names(animation)
    for name, shown in shown_by_names.items():
        ui = create_option(f"Draw {name}", layout, shown)
        # Note: connect must be out of the loop due to how variables
        #       are captured in inner functions.
        _connect_actor_ui(ui, animation, name)
    add_stretch(layout)
    return dock, layout
