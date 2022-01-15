from .shot import shot;
from .scene import scene

from PySide6.QtCore import QVariantAnimation, QAbstractAnimation, QParallelAnimationGroup, Signal, QObject


class animator(QObject):
    """
    Animate items in a shot.
    
    This can be repeated over and over to create a sequence of animations,
    creating a shot-by-shot demonstration. Each shot sets its duration in
    seconds.

    The actual animation duration can be made shorter or longer via an
    animation_speedup. As such. the shot duration is only used as a baseline
    default duration. The speedup divides the duration, so a speedup of 2 plays
    the animations twice as fast.

    The typical usage is to connect shot_ended signal to a function that sets
    up the next animation shot. Then, in each animation shot, animate() is
    called to specify which item gets animated in the shot.

    Since animate() also takes a per-animated-item on_finished callback,
    it is also possible to add new animation items when a given item is done.
    This can be useful if you want to chain animations of different items with
    different durations without having to calculate the exact chain of durations.
    """

    shot_ended = Signal(shot, scene, object)

    def __init__(self) -> None:
        """
        Creates an animator with the given default anmation duration
        and the optional animation-done callback. This callback is called
        once all animations added in animate() are done.
        """
        super().__init__()
        self.anim_speedup = 1.
        self.anims = set()
        self.anim_group = QParallelAnimationGroup()
        self.current_scene = None
        self.current_shot = None

    #################################################################
    #
    # Animations

    def animate_value(self, start_value, end_value, duration, on_changed, on_finished = None) -> None:
        """
        Animate the given scene item value.

        A value will be animated from the start_value to the end_value over the given fraction
        of the default animation duration.
        
        The given optional on_changed callback is called every time the value changes during the animation.
        The given optional on_finished is called when the animation ends.

        When all animations that were added are done, the class shot_ended is called.
        """
        anim = QVariantAnimation()
        anim.setStartValue(start_value)
        anim.setEndValue(end_value)
        if on_changed:
            anim.valueChanged.connect(on_changed)
        self.animate(anim, duration, on_finished)

    def animate(self, anim: QAbstractAnimation, duration, on_finished = None) -> None:
        """
        Add the given animation (QAbstractAnimation) the given scene item.

        A value will be animated from the start_value to the end_value over the given fraction
        of the default animation duration.
        
        The given optional on_changed callback is called every time the value changes during the animation.
        The given optional on_finished is called when the animation ends.

        When all animations that were added are done, the class shot_ended is called.
        """
        self.anims.add(anim)
        anim.setDuration(max(1., duration * 1000. / max(0.001, self.anim_speedup)))
        if on_finished:
            anim.finished.connect(on_finished)
        anim.finished.connect(lambda: self._remove_anim(anim))
        self.anim_group.addAnimation(anim)

    def play(self, shot: shot, scene: scene) -> None:
        """
        Prepare all animations by calling their prepare_anim function.
        """
        if not shot.shown:
            return
        self.current_shot = shot
        self.current_scene = scene
        for prep in shot.prepare_anims:
            prep(shot, scene, self)
        scene.ensure_all_contents_fit()
        self.anim_group.start()

    def stop(self) -> None:
        self.anim_group.stop()
        self.anim_group.clear()
        self.anims.clear()
        self.check_all_anims_done()

    def _remove_anim(self, anim: QAbstractAnimation) -> None:
        self.anims.remove(anim)
        self.anim_group.removeAnimation(anim)
        self.check_all_anims_done()

    def check_all_anims_done(self) -> None:
        if self.anims:
            return

        if not self.current_shot:
            return

        # Note: keep a copy of the current shot and scene and clear them
        #       immediately before calling cleanup of shot_ended since
        #       both may queue a new shot.
        shot = self.current_shot
        scene = self.current_scene
        self.current_shot = None
        self.current_scene = None

        for cleanup in shot.cleanup_anims:
            cleanup(shot, scene, self)

        if self.anims:
            return

        self.shot_ended.emit(shot, scene, self)


