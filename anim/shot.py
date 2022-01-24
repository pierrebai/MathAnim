from anim.scene import scene
from .named import named

class shot(named):
    """
    A shot is the basic block of an animation.

    It holds the animations that will play in a scene using an animator.
    The scene and animator will be provided by the call to the play() function.

    The shot is made of a collection of animations. Each animation is:

        - A prepare_anim function receiving the shot, scene and animator.
          The prepare_anim function adds animation to the animator.

        - A cleanup_anim function receiving the same shot, scene and animator.
    """
    def __init__(self, name: str, description: str, prep_anim: callable = None, cleanup_anim: callable = None, repeat = False):
        super().__init__(name, description)
        self.repeat = repeat
        self.reset()
        self.add_anim(prep_anim, cleanup_anim)

    def reset(self) -> None:
        """
        Resets the shot. Removes all animations.
        """
        self.prepare_anims = []
        self.cleanup_anims = []
        self.shown = True

    def show(self, shown: bool) -> None:
        """
        Shows or hides the shot.
        """
        self.shown = shown

    def add_anim(self, prep_anim: callable, cleanup_anim: callable = None) -> None:
        """
        Adds an animation to the shot. The animation is made up of:
            - An optional prepare_anim function receiving the scene and animator.
            - An optional cleanup_anim function receiving the same scene and animator.
        """
        if prep_anim:
            self.prepare_anims.append(prep_anim)
        if cleanup_anim:
            self.cleanup_anims.append(cleanup_anim)

    def _prepare(self, prep_anim, animation, scene: scene, animator) -> None:
        if callable(prep_anim):
            prep_anim(self, animation, scene, animator)
        else:
            for prep in prep_anim:
                self._prepare(prep, animation, scene, animator)

    def prepare(self, animation, scene: scene, animator) -> None:
        """
        Calls all the prep_anim functions of the shot.
        """
        self._prepare(self.prepare_anims, animation, scene, animator)

    def _cleanup(self, cleanup_anim, animation, scene: scene, animator) -> None:
        if callable(cleanup_anim):
            cleanup_anim(self, animation, scene, animator)
        else:
            for prep in cleanup_anim:
                self._cleanup(prep, animation, scene, animator)

    def cleanup(self, animation, scene: scene, animator) -> None:
        """
        Calls all the cleanup_anim functions of the shot.
        """
        self._cleanup(self.cleanup_anims, animation, scene, animator)
