from .scene import scene
from .animator import animator

class shot:
    """
    Holds the actors that will play in the shot in a scene using an animator.
    The scene and animator will be provided in the play() function.

    The shot is made of a collection of animations. Each animation is:
        - A prepare_anim function receiving the scene and animator.
        - A cleanup_anim function receiving the same scene and animator.
    """
    def __init__(self, description, prep_anim = None, cleanup_anim = None):
        self.description = description
        self.reset()
        self.add_anim(prep_anim, cleanup_anim)

    def reset(self):
        """
        Resets the shot. Removes all animations.
        """
        self.prepare_anims = []
        self.cleanup_anims = []
        self.scene = None
        self.animator = None

    def add_anim(self, prep_anim, cleanup_anim = None):
        """
        Add an animation to the shot. The animation is made up of:
            - An optional prepare_anim function receiving the scene and animator.
            - An optional cleanup_anim function receiving the same scene and animator.
        """
        if prep_anim:
            self.prepare_anims.append(prep_anim)
        if cleanup_anim:
            self.cleanup_anims(cleanup_anim)

    def shot_done(self):
        """
        Cleanup all animations by calling their cleanup_anim function.
        """
        for cleanup in self.cleanup_anims:
            cleanup(self.scene, self.animator)

    def play(self, scene: scene, animator: animator):
        """
        Prepare all animations by calling their prepare_anim function.
        """
        self.scene = scene
        self.animator = animator
        for prep in self.prepare_anims:
            prep(scene, animator)

    @staticmethod
    def play_all(shots, scene: scene, animator: animator):
        """
        Play all shots by calling their play function.
        shots can contain sub-list of shots and can contain None.
        The sub-list are also played, the None are skipped.
        """
        for s in shots:
            if type(s) is shot:
                s.play(scene, animator)
            elif s:
                shot.play_all(s, scene, animator)
