from .ui import *
from ..animation import animation
from ..animator import animator
from ..options import option
from ..scene import scene

from PySide6.QtWidgets import *

from typing import Tuple

def _add_ui_description(ui: QWidget, option: option) -> None:
    """
    Adds the option description as a tooltip on the UI.
    """
    if not option.description:
        return
    ui.setToolTip(option.description)
    
def _create_int_ui(option: option, scene: scene, animation: animation, animator: animator, layout: QLayout) -> None:
    ui = create_number_range_slider(option.name, option.low_value, option.high_value, option.value, layout)
    _add_ui_description(ui, option)

    def on_changed(value):
        try:
            option.value = int(value)
            scene.view.preserve_transform()
            animation.option_changed(scene, animator, option)
        except:
            pass
    connect_auto_signal(ui, ui.valueChanged, on_changed)

def _create_float_ui(option: option, scene: scene, animation: animation, animator: animator, layout: QLayout) -> None:
    ui = create_number_text(option.name, option.low_value, option.high_value, option.value, layout)
    _add_ui_description(ui, option)
    def on_changed(value):
        try:
            option.value = float(value)
            scene.view.preserve_transform()
            animation.option_changed(scene, animator, option)
        except:
            pass
    connect_auto_signal(ui, ui.textChanged, on_changed)

def _create_bool_ui(option: option, scene: scene, animation: animation, animator: animator, layout: QLayout) -> None:
    ui = create_checkbox(option.name, layout, option.value)
    _add_ui_description(ui, option)
    def on_changed(state):
        try:
            option.value = bool(state)
            scene.view.preserve_transform()
            animation.option_changed(scene, animator, option)
        except:
            pass
    connect_auto_signal(ui, ui.stateChanged, on_changed)

def _create_list_ui(option: option, scene: scene, animation: animation, animator: animator, layout: QLayout) -> None:
    items = [(name, "") for name in option.low_value]
    ui = create_list(option.name, items, layout)
    _add_ui_description(ui, option)
    def on_changed(value):
        try:
            option.value = str(value)
            scene.view.preserve_transform()
            animation.option_changed(scene, animator, option)
        except:
            pass
    connect_auto_signal(ui, ui.currentTextChanged, on_changed)

def _create_text_ui(option: option, scene: scene, animation: animation, animator: animator, layout: QLayout) -> None:
    ui = create_text(option.name, option.description, option.value, layout)
    _add_ui_description(ui, option)
    def on_changed(value):
        try:
            option.value = str(value)
            scene.view.preserve_transform()
            animation.option_changed(scene, animator, option)
        except:
            pass
    connect_auto_signal(ui, ui.textChanged, on_changed)

_ui_makers = {
    int: _create_int_ui,
    float: _create_float_ui,
    bool: _create_bool_ui,
    list: _create_list_ui,
    str: _create_text_ui,
}

def create_option_ui(option: option, scene: scene, animation: animation, animator: animator, layout) -> None:
    """
    Create the UI for a single option.
    """
    try:
        maker = _ui_makers[type(option.low_value if option.low_value else option.value)]
    except:
        return None
    return maker(option, scene, animation, animator, layout)

def _fill_options_ui(scene: scene, animation: animation, animator: animator, layout: QVBoxLayout) -> None:
    for option in animation.options:
        create_option_ui(option, scene, animation, animator, layout)
    add_stretch(layout)

def create_options_ui(scene: scene, animation: animation, animator: animator) -> Tuple[QDockWidget, QVBoxLayout]:
    """
    Creates the UI to control the animation options.
    """
    dock, layout = create_dock("Animation Options")
    _fill_options_ui(scene, animation, animator, layout)
    return dock, layout

def update_options_ui(scene: scene, animation: animation, animator: animator, dock: QDockWidget, layout: QVBoxLayout) -> QVBoxLayout:
    layout = empty_dock(dock, layout)
    _fill_options_ui(scene, animation, animator, layout)
    return layout
