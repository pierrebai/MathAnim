from .ui import create_dock, create_list, empty_dock, add_stretch, connect_auto_signal
from ..animation import animation

from PySide6.QtWidgets import QDockWidget, QVBoxLayout

from typing import Tuple, List

def _fill_animations_ui(animations: List[Tuple[str, str]], on_changed: callable, layout: QVBoxLayout) -> None:
    ui = create_list("Animations", animations, layout)
    if on_changed:    
        connect_auto_signal(ui, ui.currentTextChanged, on_changed)
    add_stretch(layout)

def create_animations_ui(animations: List[Tuple[str, str]], on_changed: callable) -> Tuple[QDockWidget, QVBoxLayout]:
    """
    Creates the UI showning the list of animations.
    """
    dock, layout = create_dock("Animations")
    _fill_animations_ui(animations, on_changed, layout)
    return dock, layout

def update_animations_ui(animations: List[Tuple[str, str]], on_changed: callable, dock: QDockWidget, layout: QVBoxLayout) -> QVBoxLayout:
    layout = empty_dock(dock, layout)
    _fill_animations_ui(animations, on_changed, layout)
    return layout
