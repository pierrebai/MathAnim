from sqlite3 import connect
from ..named import named

from PySide6.QtCore import QTimer, Qt, Signal, QKeyCombination
from PySide6.QtWidgets import *
from PySide6.QtGui import QIntValidator, QDoubleValidator, QShortcut, QKeySequence 

from typing import Tuple, Union, List

IntOrFloat = Union[int, float]


############################################################################
#
# App

def create_app() -> QApplication:
    """
    Creates and returns the QApplication with the command-line arguments.
    """
    import sys
    return QApplication(sys.argv)

def start_app(app: QApplication, window: QMainWindow) -> None:
    """
    Starts the given application with the given main window.
    """
    window.show()
    app.exec_()


############################################################################
#
# Dock

def _create_dock_container(dock: QDockWidget) -> QVBoxLayout:
    container = QWidget()
    container.setMinimumWidth(150)
    container.setMaximumWidth(350)
    layout = QVBoxLayout(container)
    dock.setWidget(container)
    return layout

def create_dock(title: str) -> Tuple[QDockWidget, QVBoxLayout]:
    """
    Creates a QDockWidget that can be put in a QMainWindow
    and creates a vertical layout (QVBoxLayout) in the dock.
    Returns both.
    """
    dock = QDockWidget(title)
    dock.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
    layout = _create_dock_container(dock)
    return dock, layout

def disconnect_dock(dock: QDockWidget, layout: QVBoxLayout) -> None:
    for i in range(layout.count()):
        item = layout.itemAt(i)
        ui = item.widget()
        if ui:
            disconnect_auto_signals(ui)

def empty_dock(dock: QDockWidget, layout: QVBoxLayout) -> QVBoxLayout:
    disconnect_dock(dock, layout)
    while layout.count():
        item = layout.itemAt(layout.count() - 1)
        ui = item.widget()
        if ui:
            layout.removeWidget(ui)
        else:
            layout.removeItem(item)
    return _create_dock_container(dock)

def add_stretch(layout: QLayout) -> None:
    """
    Adds a stretcheable zone to a layout.
    """
    layout.addStretch()


############################################################################
#
# List UI ELement

def create_list(title: str, contents: List[Tuple[str, str]], layout: QLayout, enabled = True) -> QListWidget:
    """
    Creates and returns a list widget with the given title and contents
    in the given layout. The list can optionally be disabled.
    """
    create_label(title, layout)
    widget = QListWidget()
    widget.setEnabled(enabled)
    for name, description in contents:
        widget.addItem(name)
        if description:
            item = widget.item(widget.count() - 1)
            item.setToolTip(description)
    layout.addWidget(widget)
    return widget

def create_named_list(title: str, contents: List[named], layout: QLayout, enabled = True) -> QListWidget:
    """
    Creates and returns a list widget with the given title and
    named objects as contents in the given layout. The list can
    optionally be disabled.
    """
    return create_list(title, [(item.name, item.description) for item in contents], layout, enabled)

def select_in_list(name: str, widget: QListWidget) -> None:
    """
    Selects the item with the given text in the list widget.
    """
    items = widget.findItems(name, Qt.MatchExactly)
    if len(items) > 0:
        widget.setCurrentItem(items[0])


############################################################################
#
# UI Elements

def create_label(title: str, layout: QLayout) -> QLabel:
    """
    Creates and returns a label in the given layout with the given text.
    """
    widget = QLabel(title)
    layout.addWidget(widget)
    return widget

def create_button(title: str, layout: QLayout) -> QPushButton:
    """
    Creates and returns a QPushButton with the given text in the given layout.
    """
    widget = QPushButton(title)
    layout.addWidget(widget)
    return widget

def add_button_shortcut(button: QPushButton, key: Union[QKeySequence, QKeyCombination, Qt.Key]) -> QShortcut:
    """
    Adds a shortcut for the given button.
    """
    if isinstance(key, Qt.Key):
        key = QKeyCombination(key)
    if isinstance(key, QKeyCombination):
        key = QKeySequence(key)
    shortcut = QShortcut(key, button)
    shortcut.activated.connect(button.animateClick)
    return shortcut    

def create_horiz_container(layout: QLayout) -> QHBoxLayout:
    """
    Creates and returns a horizontal layout (QHBoxLayout).
    """
    container = QWidget()
    container_layout = QHBoxLayout(container)
    container_layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(container)
    return container_layout

def create_number_range(title: str, low: int, high: int, value: int, layout: QLayout) -> QSpinBox:
    """
    Creates and returns an integer number widget (QSpinBox) with the given title,
    the given low and high limits and current value, in the given layout.
    """
    container_layout = create_horiz_container(layout)
    if title:
        create_label(title, container_layout)
    widget = QSpinBox()
    widget.setRange(low, high)
    widget.setValue(value)
    container_layout.addWidget(widget)
    return widget

def create_text(title: str, example: str, value: str, layout: QLayout) -> QLineEdit:
    """
    Creates and retursn a one-line text editing widget (QLineEdit)
    with the given title, example contents and current value in the given layout.
    """
    container_layout = create_horiz_container(layout)
    if title:
        create_label(title, container_layout)
    widget = QLineEdit()
    widget.setText(value)
    widget.setPlaceholderText(example)
    container_layout.addWidget(widget)
    return widget

def create_read_only_text(title: str, example: str, value: str, layout: QLayout) -> QLineEdit:
    """
    Creates and returns a read-only one-line text widget (QLineEdit)
    with the given title, example contents and value in the given layout.
    """
    widget = create_text(title, example, value, layout)
    widget.setEnabled(False)
    return widget

def create_number_text(title: str, low: IntOrFloat, high: IntOrFloat, value: IntOrFloat, layout: QLayout) -> QLineEdit:
    """
    Creates and returns a one-line text widget (QLineEdit) for an integer
    or floating-point number, with the given title, low and high limits,
    and current value in the given layout.
    """
    widget = create_text(title, str((low + high)/2), str(value), layout)
    if isinstance(value, int):
        widget.setValidator(QIntValidator(low, high))
    return widget

def create_number_slider(title: str, low: int, high: int, value: int, layout: QLayout) -> QSlider:
    """
    Creates and returns a slider widget (QSlider) for an integer number,
    with the given title, low and high limits, and current value in the given layout.
    """
    container_layout = create_horiz_container(layout)
    if title:
        create_label(title, container_layout)
    widget = QSlider()
    widget.setMinimum(low)
    widget.setMaximum(high)
    widget.setValue(value)
    widget.setOrientation(Qt.Horizontal)
    delta = high - low
    if delta > 20:
        widget.setPageStep(delta // 10)
    if delta > 100:
        widget.setSingleStep(delta // 100)
    container_layout.addWidget(widget)
    return widget

def create_number_range_slider(title: str, low: int, high: int, value: int, layout: QLayout) -> QLineEdit:
    """
    Creates both a text widget (QLineEdit) and a slider widget (QSlider) for an integer number,
    with the given title, low and high limits, and current value in the given layout.
    The widgets value-changed signals are connected to each other's setValue slot.
    The text widget is returned.
    """
    text = create_number_range(title, low, high, value, layout)
    slider = create_number_slider("", low, high, value, layout)
    text.valueChanged.connect(slider.setValue)
    slider.valueChanged.connect(text.setValue)
    return text

def create_checkbox(title: str, layout: QLayout, state = True) -> QCheckBox:
    """
    Creates and returns an option widget (QCheckBox) with teh given title in the given layout.
    Optionally set the current state, which defaults to True.
    """
    widget = QCheckBox(title)
    widget.setChecked(state)
    layout.addWidget(widget)
    return widget

def create_main_window(title: str, central_widget) -> QMainWindow:
    """
    Creates and returns a main window (QMainWindow) with the given title and central widget.
    """
    window = QMainWindow()
    window.setWindowTitle(title)
    window.resize(1280, 800)
    window.setCentralWidget(central_widget)
    return window

def add_dock(window: QMainWindow, dock: QDockWidget, area = Qt.LeftDockWidgetArea) -> None:
    """
    Adds a dockable widget to the given main window in the given area, left area by default.
    """
    window.addDockWidget(area, dock)

def create_timer(interval: int) -> QTimer:
    """
    Creates a timer with the given milliseconds interval.
    """
    timer = QTimer()
    timer.setInterval(interval)
    return timer


############################################################################
#
# Signals

def connect_auto_signal(obj: object, signal: Signal, func: callable):
    """
    Connects the signal to the callable and adds the signal connection
    to the auto_disconnect variable of the object, so it can be disconnected
    later by disconnect_auto_signals().
    """
    connection = signal.connect(func)

    if not hasattr(obj, "auto_disconnect"):
        obj.auto_disconnect = []
    obj.auto_disconnect.append((signal, connection))

def disconnect_auto_signals(obj: object):
    """
    Disconnects all registered signal.
    """
    if not hasattr(obj, "auto_disconnect"):
        return
    for signal, connection in obj.auto_disconnect:
        signal.disconnect(connection)
    obj.auto_disconnect.clear()
