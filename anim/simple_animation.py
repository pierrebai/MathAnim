from .actor import actor
from .animation import animation
from .animator import animator
from .options import option
from .scene import scene
from .shot import shot

from typing import Dict, Any, List, Tuple

import modulefinder

class simple_animation(animation):
    """
    A simple animation made from the global variables of a module.
    """

    @staticmethod
    def _is_of_type(var, type) -> bool:
        if isinstance(var, list) and len(var):
            return simple_animation._is_of_type(var[0], type)
        elif isinstance(var, tuple) and len(var):
            return simple_animation._is_of_type(var[0], type)
        else:
            return isinstance(var, type)

    @staticmethod
    def from_module(module_dict: Dict[str, Any]) -> callable:
        """
        Create an animation from the global variables of a module.

        The variables that are looked-for are:

            - name: the name of the animation.
            - description: the description of the animation.
            - loop: if the animation should loop when reaching the last shot. Defaults to False.
            - reset_on_change: should the animation reset when options change. Defaults to True.
            - Variables that are instances of the shot class.
            - Variables that are instances of the actor class.
            - Variables that are instances of the option class.
            - generate_actors: a function that generates actors.
            - generate_shots: a function that generates shots.
            - reset: a function to reset the animation.
            - option_changed: a function that reacts to changing options.
            - shot_ended: a function called when an aniamtion shot ends.

        Only name, description and either shots or generate_shots are
        required. The others are optional.
        """
        name = None
        description = None
        loop = False
        reset_on_change = True
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
            elif var_name == 'loop':
                loop = var
            elif var_name == 'reset_on_change':
                reset_on_change = var
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
            elif simple_animation._is_of_type(var, shot):
                shots.append(var)
            elif simple_animation._is_of_type(var, actor):
                actors.append(var)
            elif simple_animation._is_of_type(var, option):
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
                name, description, loop, reset_on_change, shots, actors, options,
                custom_generate_actors, custom_generate_shots, custom_reset,
                custom_option_changed, custom_shot_ended)
        return maker

    def __init__(self, name, description, loop, reset_on_change,
                 shots, actors, options,
                 custom_generate_actors, custom_generate_shots,
                 custom_reset, custom_option_changed, custom_shot_ended) -> None:
        super().__init__(name, description)
        self.loop = loop
        self.reset_on_change = reset_on_change
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
    