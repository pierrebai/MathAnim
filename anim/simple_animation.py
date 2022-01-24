from .actor import actor
from .animation import animation
from .animator import animator
from .options import option
from .scene import scene
from .shot import shot

from typing import Dict, Any, List, Tuple

import modulefinder

class simple_animation(animation):

    @staticmethod
    def from_module(module_dict: Dict[str, Any]) -> callable:
        name = None
        description = None
        shots = []
        actors = []
        options = []
        custom_generate_actors = None
        custom_generate_shots = None
        custom_reset = None
        custom_option_changed = None
        custom_shot_ended = None

        for var_name, var in module_dict.items():
            if var_name.startswith('_'):
                continue

            if var_name == 'name':
                name = var
            elif var_name == 'description':
                description = var
            elif var_name == 'generate_actors':
                custom_generate_actors = var
            elif var_name == 'generate_shots':
                custom_generate_shots = var
            elif var_name == 'reset':
                custom_reset = var
            elif var_name == 'option_changed':
                custom_option_changed = var
            elif var_name == 'shot_ended':
                custom_shot_ended = var
            elif isinstance(var, shot):
                shots.append(var)
            elif isinstance(var, actor):
                actors.append(var)
            elif isinstance(var, option):
                options.append(var)
            elif isinstance(var, list) and len(var):
                if isinstance(var[0], shot):
                    shots.append(var)
                elif isinstance(var[0], actor):
                    actors.append(var)
                elif isinstance(var[0], option):
                    options.append(var)

        # Validate. No options and no actors are OK.
        errors = []
        if not name:
            errors.append("No animation name defined. Declare a 'name' global variable.")

        if not description:
            errors.append("No animation description defined. Declare a 'description' global variable.")

        if not shots and not custom_generate_shots:
            errors.append("No animation shot defined. Declare instances of the anim.shot class as global variable or a function named 'generate_shots'.")

        if errors:
            print('\n'.join(errors))
            return None

        def maker():
            return simple_animation(
                name, description, shots, actors, options,
                custom_generate_actors, custom_generate_shots, custom_reset,
                custom_option_changed, custom_shot_ended)
        return maker

    def __init__(self, name, description,
                 shots, actors, options,
                 custom_generate_actors, custom_generate_shots,
                 custom_reset, custom_option_changed, custom_shot_ended) -> None:
        super().__init__(name, description)
        self.custom_shots = shots
        self.custom_actors = actors
        self.custom_generate_actors = custom_generate_actors
        self.custom_generate_shots = custom_generate_shots
        self.custom_reset = custom_reset
        self.custom_option_changed = custom_option_changed
        self.custom_shot_ended = custom_shot_ended
        self.add_options(options)

    def generate_actors(self, scene: scene) -> None:
        super().generate_actors(scene)
        self.add_actors(self.custom_actors, scene)
        if self.custom_generate_actors:
            self.custom_generate_actors(self, scene)

    def generate_shots(self) -> None:
        super().generate_shots()
        self.add_shots(self.custom_shots)
        if self.custom_generate_shots:
            self.custom_generate_shots(self)

    def reset(self, scene: scene, animator: animator) -> None:
        super().reset(scene, animator)
        if self.custom_reset:
            self.custom_reset(self, scene, animator)

    def option_changed(self, scene: scene, animator: animator, option: option) -> None:
        super().option_changed(scene, animator, option)
        if self.custom_option_changed:
            self.custom_option_changed(self, scene, animator, option)

    def shot_ended(self, ended_shot: shot, ended_scene: scene, ended_animator: animator):
        super().shot_ended(ended_shot, ended_scene, ended_animator)
        if self.custom_shot_ended:
            self.custom_shot_ended(self, ended_shot, ended_scene, ended_animator)
    