from .named import named
from .actor import actor
from .shot import shot
from .options import option, options
from .scene import scene

class animation(named):
    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.actors = set()
        self.shots = []
        self.options = options()

    def reset(self, scene: scene) -> None:
        """
        Clears the actors and shots.
        """
        for actor in self.actors:
            scene.remove_actor(actor)
        self.actors = set()
        self.shots = []

    def add_actors(self, actors, scene: scene = None) -> None:
        """
        Add actors that participates in the animation.
        Having a list of actors allows turning them on and off.

        The actors can be a single actor, a list of actors or a list of lists, etc.
        (Actually supports any iterable.)
        """
        if isinstance(actors, actor):
            self.actors.add(actors)
            if scene:
                scene.add_actor(actors)
        else:
            for a in actors:
                self.add_actors(a, scene)

    def add_shots(self, shots) -> None:
        """
        Add shots to the animation.
        Having a list of shots allows playing them and turning them on and off.

        The shots can be a single shot, a list of shots or a list of lists, etc.
        (Actually supports any iterable.)
        """
        if isinstance(shots, shot):
            self.shots.append(shots)
        else:
            for a in shots:
                self.add_shots(a)

    def add_options(self, options) -> None:
        """
        Add animation options.
        Having a list of options allows the user to modify them.

        The options can be a single option, a list of options or a list of lists, etc.
        (Actually supports any iterable.)
        """
        if isinstance(options, option):
            self.options.append(options)
        else:
            for opt in options:
                self.add_options(opt)

    def option_changed(self, scene: scene, option: option) -> None:
        """
        Called when an option value is changed.
        Override in sub-classes to react to option changes.
        """
        pass
