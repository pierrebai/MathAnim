from .actor import actor
from .animation import animation
from .animator import animator
from .options import option
from .scene import scene
from .shot import shot
from .algorithms import is_of_type

from typing import Dict as _Dict, Any as _Any, List as _List, Tuple as _Tuple, Callable as _Callable

class anim_description:
    """
    A description of a simple animation made from the global variables of a module.
    """
    def __init__(self):
        self.name: str = None
        self.description: str = None
        self.loop: bool = False
        self.reset_on_change: bool = True
        self.has_pointing_arrow: bool = True
        self.auto_framing = True
        self.frame_on_start = True
        self.shots: _List[shot] = []
        self.actors: _List[actor] = []
        self.options: _List[option] = []
        self.custom_generate_actors: _Callable = None
        self.custom_generate_shots: _Callable = None
        self.custom_reset: _Callable = None
        self.custom_prepare_playing: _Callable = None
        self.custom_option_changed: _Callable = None
        self.custom_shot_ended: _Callable = None

    def _scan_module(self, module_dict: _Dict[str, _Any]) -> _List[_Callable]:
        prep_shots: _List[_Callable] = []

        for var_name, var in module_dict.items():
            if var_name.startswith('_'):
                continue

            if var_name == 'name':
                self.name = var
            elif var_name == 'description':
                self.description = var
            elif var_name == 'loop':
                self.loop = var
            elif var_name == 'reset_on_change':
                self.reset_on_change = var
            elif var_name == 'has_pointing_arrow':
                self.has_pointing_arrow = var
            elif var_name == 'frame_on_start':
                self.frame_on_start = var
            elif var_name == 'auto_framing':
                self.auto_framing = var
            elif var_name == 'generate_actors':
                self.custom_generate_actors = var
            elif var_name == 'generate_shots':
                self.custom_generate_shots = var
            elif var_name == 'reset':
                self.custom_reset = var
            elif var_name == 'prepare_playing':
                self.custom_prepare_playing = var
            elif var_name == 'option_changed':
                self.custom_option_changed = var
            elif var_name == 'shot_ended':
                self.custom_shot_ended = var
            elif callable(var) and var_name.endswith('_shot'):
                prep_shots.append(var)
            elif is_of_type(var, shot):
                self.shots.append(var)
            elif is_of_type(var, actor):
                self.actors.append(var)
            elif is_of_type(var, option):
                self.options.append(var)

        return prep_shots

    @staticmethod
    def create_shot(prep):
        shot_name = ""
        shot_description = ""
        if prep.__doc__:
            lines: list[str] = prep.__doc__.strip().splitlines()
            shot_name = lines[0] if lines else '-'
            if len(lines) > 1:
                first_line = 1
                while not lines[first_line].strip():
                    first_line += 1
                shot_description = '\n'.join(lines[first_line:])
        return shot(shot_name, shot_description, prep)

    def create_shots(self, prep_shots: _List[_Callable]):
        for prep in prep_shots:
            self.shots.append(anim_description.create_shot(prep))

    def _validate(self):
        # Validate. No options and no actors are OK.
        errors = []
        if not self.name:
            errors.append("No animation name defined. Declare a 'name' global variable.")

        if not self.description:
            errors.append("No animation description defined. Declare a 'description' global variable.")

        if not self.shots and not self.custom_generate_shots:
            errors.append(
                "No animation shot defined. Declare instances of the anim.shot class as global variables"
                " or a function named 'generate_shots' or functions with names ending in _shot.")

        if errors:
            print('\n'.join(errors))
            return None


class simple_animation(animation, anim_description):
    """
    A simple animation made from the global variables of a module.
    """

    @staticmethod
    def from_module(module_dict: _Dict[str, _Any]) -> _Callable:
        """
        Create a function that will create an animation from the global variables of a module.

        The variables that are looked-for are:

            - name: the name of the animation.
            - description: the description of the animation.
            - loop: if the animation should loop when reaching the last shot. Defaults to False.
            - reset_on_change: should the animation reset when options change. Defaults to True.
            - has_pointing_arrow: does the animation uses the pointing arrow. Default to True.
            - auto_framing: frame all contents at the start of each shot.
            - *_shot: the anim-preparation function of a shot, a shot will be created with the first
                      line of the function doc as the name and the rest as its description.
            - Variables that are instances of the shot class.
            - Variables that are instances of the actor class.
            - Variables that are instances of the option class.
            - generate_actors: a function that generates actors.
            - generate_shots: a function that generates shots.
            - reset: a function to reset the animation.
            - option_changed: a function that reacts to changing options.
            - shot_ended: a function called when an animation shot ends.

        Only name, description and either shots or generate_shots are
        required. The others are optional.
        """

        desc = anim_description()
        prep_shots = desc._scan_module(module_dict)
        desc.create_shots(prep_shots)
        desc._validate()

        def maker():
            return simple_animation(desc)
        return maker

    def __init__(self, desc: anim_description) -> None:
        super().__init__(desc.name, desc.description)
        self.loop = desc.loop
        self.reset_on_change = desc.reset_on_change
        self.has_pointing_arrow = desc.has_pointing_arrow
        self.auto_framing = desc.auto_framing
        self.frame_on_start = desc.frame_on_start
        self.custom_shots = desc.shots
        self.custom_actors = desc.actors
        self.custom_generate_actors = desc.custom_generate_actors
        self.custom_generate_shots = desc.custom_generate_shots
        self.custom_reset = desc.custom_reset
        self.custom_prepare_playing = desc.custom_prepare_playing
        self.custom_option_changed = desc.custom_option_changed
        self.custom_shot_ended = desc.custom_shot_ended
        self.add_options(desc.options)

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
        if not self.has_pointing_arrow:
            self.remove_pointing_arrow(scene)

    def prepare_playing(self, scene: scene, animator: animator) -> None:
        super().prepare_playing(scene, animator)
        if self.custom_prepare_playing:
            self.custom_prepare_playing(self, scene, animator)

    def option_changed(self, scene: scene, animator: animator, option: option) -> None:
        super().option_changed(scene, animator, option)
        if self.custom_option_changed:
            self.custom_option_changed(self, scene, animator, option)

    def shot_ended(self, ended_shot: shot, ended_scene: scene, ended_animator: animator):
        super().shot_ended(ended_shot, ended_scene, ended_animator)
        if self.custom_shot_ended:
            self.custom_shot_ended(self, ended_shot, ended_scene, ended_animator)
    