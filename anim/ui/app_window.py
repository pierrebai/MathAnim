from anim.options import option
from ..animation import animation
from ..animator import animator
from ..scene import scene

from .ui import *
from .options_ui import create_options_ui, update_options_ui
from .actors_ui import create_actors_ui, update_actors_ui
from .shots_ui import create_shots_ui, update_shots_ui
from .animations_ui import create_animations_ui
from .animation_controls_ui import create_animation_controls_ui, update_animation_controls_ui

from typing import List, Type, Tuple

def create_app_window(animations: List[Tuple[str, Type]], scene: scene, animator: animator) -> QMainWindow:
    if not animations:
        return

    current_anim = animations[0][1](scene, animator)
    anim_ctrl_dock, anim_ctrl_layout = create_animation_controls_ui(current_anim, scene, animator)
    options_dock, options_layout = create_options_ui(scene, current_anim, animator)
    actors_dock, actors_layout = create_actors_ui(current_anim)
    shots_dock, shots_layout = create_shots_ui(current_anim)

    def on_anim_changed(name: str):
        nonlocal anim_ctrl_layout, options_layout, actors_layout, shots_layout, window
        for anim_name, anim_type in animations:
            if anim_name == name:
                animator.stop()
                animator.reset()
                scene.reset()
                current_anim = anim_type(scene, animator)
                anim_ctrl_layout = update_animation_controls_ui(current_anim, scene, animator, anim_ctrl_dock, anim_ctrl_layout)
                options_layout = update_options_ui(scene, current_anim, animator, options_dock, options_layout)
                actors_layout = update_actors_ui(current_anim, actors_dock, actors_layout)
                shots_layout = update_shots_ui(current_anim, shots_dock, shots_layout)
                break

    anims_dock, _ = create_animations_ui([anim_name for anim_name, _ in animations], on_anim_changed)

    window = create_main_window(current_anim.name, scene.get_widget())
    add_dock(window, anims_dock)
    add_dock(window, shots_dock)
    add_dock(window, anim_ctrl_dock)
    add_dock(window, options_dock)
    add_dock(window, actors_dock)

    return window
