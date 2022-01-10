from .named import named
from .ui import *

class option(named):
    def __init__(self, name: str, description: str, value, low_value: None, high_value: None) -> None:
        super().__init__(name, description)
        self.value = value
        self.low_value = low_value
        self.high_value = high_value
        self.default_value = value

    def reset(self):
        self.value = self.default_value

    def create_ui(self, scene, animation, animator, layout):
        try:
            maker = ui_makers[type(self.value)]
        except:
            return None
        return maker(self, scene, animation, animator, layout)

def _create_int_ui(option: option, scene, animation, animator, layout: QLayout) -> None:
    # TODO: add description as tooltip.
    ui = create_number_range_slider(option.name, option.low_value, option.high_value, option.value, layout)
    @ui.valueChanged.connect
    def on_changed(value):
        option.value = int(value)
        animation.option_changed(scene, animator, option)

def _create_float_ui(option: option, scene, animation, animator, layout: QLayout) -> None:
    # TODO: add description as tooltip.
    ui = create_number_text(option.name, option.low_value, option.high_value, option.value, layout)
    @ui.valueChanged.connect
    def on_changed(value):
        option.value = float(value)
        option.animation.option_changed(scene, animator, option)

def _create_bool_ui(option: option, scene, animation, animator, layout: QLayout) -> None:
    # TODO: add description as tooltip.
    ui = create_option(option.name, layout, option.value)
    @ui.stateChanged.connect
    def on_changed(state):
        option.value = bool(state)
        option.animation.option_changed(scene, animator, option)

def _create_list_ui(option: option, scene, animator, layout: QLayout) -> None:
    # TODO: add description as tooltip.
    ui = create_list(option.name, option.low_value, layout)
    # TODO: list change reaction.

def _create_text_ui(option: option, scene, animation, animator, layout: QLayout) -> None:
    ui = create_text(option.name, option.description, option.value, layout)
    @ui.textChanged.connect
    def on_changed(value):
        option.value = str(value)
        option.animation.option_changed(scene, animator, option)

ui_makers = {
    int: _create_int_ui,
    float: _create_float_ui,
    bool: _create_bool_ui,
    list: _create_list_ui,
    str: _create_text_ui,
}

options = list


