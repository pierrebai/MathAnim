from .named import named
from .actor import actor
from .animator import animator
from .shot import shot
from .options import option, options
from .scene import scene

class animation(named):
    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.options = options()
        self.actors = set()
        self.shots = []
        self.current_shot = -1
        self.playing = False
        self.on_shot_changed = None

    def reset(self, scene: scene) -> None:
        """
        Clears the actors and shots.
        """
        for actor in self.actors:
            scene.remove_actor(actor)
        self.actors = set()
        self.shots = []

    def add_actors(self, actors, scene: scene) -> None:
        """
        Add actors that participates in the animation.
        Having a list of actors allows turning them on and off.

        The actors can be a single actor, a list of actors or a list of lists, etc.
        (Actually supports any iterable.)
        """
        if isinstance(actors, actor):
            self.actors.add(actors)
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

    def option_changed(self, scene: scene, animator: animator, option: option) -> None:
        """
        Called when an option value is changed.
        Override in sub-classes to react to option changes.
        """
        pass

    def play(self, scene: scene, animator: animator, start_at_shot = 0) -> None:
        if self.playing:
            return
        self.playing = True
        if not start_at_shot is None:
            self.current_shot = start_at_shot - 1
        self.play_next_shot(scene, animator)

    def play_next_shot(self, scene: scene, animator: animator) -> None:
        self.current_shot = self.current_shot + 1
        self.play_current_shot(scene, animator)

    def play_current_shot(self, scene: scene, animator: animator) -> None:
        if not self.playing or not self.shots:
            return
        self.current_shot = self.current_shot % len(self.shots)
        shot = self.shots[self.current_shot]
        shot.play(scene, animator)
        scene.ensure_all_contents_fit()
        animator.play()
        if self.on_shot_changed:
            self.on_shot_changed(scene, animator, shot)

    def stop(self, animator: animator) -> None:
        if not self.playing:
            return
        self.playing = False
        animator.stop()
