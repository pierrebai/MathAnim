from .actor import actor
from .animation import animation
from .animator import animator
from .options import option
from .scene import scene
from .shot import shot

class simple_animation(animation):

    def __init__(self) -> None:
        name = "" # TODO scan
        description = "" # TODO scan
        super().__init__(name, description, scene, animator)

    def generate_actors(self, scene: scene) -> None:
        pass

    def generate_shots(self) -> None:
        pass

    def reset(self, scene: scene, animator: animator) -> None:
        pass

    def option_changed(self, scene: scene, animator: animator, option: option) -> None:
        pass

    def shot_ended(self, ended_shot: shot, ended_scene: scene, ended_animator: animator):
        pass
    