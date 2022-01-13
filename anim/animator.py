from PyQt5.QtCore import QEasingCurve, QVariant, QVariantAnimation, QAbstractAnimation, QParallelAnimationGroup
from PyQt5.QtWidgets import QGraphicsItem


class animator:
    """
    Animate items in a shot.
    
    This can be repeated over and over to create a sequence of animations,
    creating a shot-by-shot demonstration. Each shot sets its duration in
    seconds.

    The actual animation duration can be made shorter or longer via an
    animation_speedup. As such. the shot duration is only used as a baseline
    default duration. The speedup divides the duration, so a speedup of 2 plays
    the animations twice as fast.

    The typical usage is to given a anim_done_callback when creating the
    animator that sets up the next animation shot. In each animation shot,
    animate() is called multiple times to specify which item gets animated.

    Since animate() also takes a per-animated-item on_finished callback,
    it is also possible to add new animation items when a given item is done.
    This can be useful if you want to chain animations of different items with
    different durations without having to calculate the exact chain of durations.
    """

    def __init__(self, anim_done_callback = None):
        """
        Creates an animator with the given default anmation duration
        and the optional animation-done callback. This callback is called
        once all animations added in animate() are done.
        """
        self.anim_done_callback = anim_done_callback
        self.anim_speedup = 1.
        self.anims = set()
        self.anim_group = QParallelAnimationGroup()


    #################################################################
    #
    # Animations

    def animate_value(self, start_value, end_value, duration, on_changed, on_finished = None) -> QAbstractAnimation:
        """
        Animate the given scene item value.

        A value will be animated from the start_value to the end_value over the given fraction
        of the default animation duration.
        
        The given optional on_changed callback is called every time the value changes during the animation.
        The given optional on_finished is called when the animation ends.

        When all animations that were added are done, the class anim_done_callback is called.
        """
        anim = QVariantAnimation()
        anim.setStartValue(QVariant(start_value))
        anim.setEndValue(QVariant(end_value))
        if on_changed:
            anim.valueChanged.connect(on_changed)
        return self.animate(anim, duration, on_finished)

    def animate(self, anim: QAbstractAnimation, duration, on_finished = None) -> QAbstractAnimation:
        """
        Add the given animation (QAbstractAnimation) the given scene item.

        A value will be animated from the start_value to the end_value over the given fraction
        of the default animation duration.
        
        The given optional on_changed callback is called every time the value changes during the animation.
        The given optional on_finished is called when the animation ends.

        When all animations that were added are done, the class anim_done_callback is called.
        """
        self.anims.add(anim)
        anim.setDuration(max(1., duration * 1000. / max(0.001, self.anim_speedup)))
        if on_finished:
            anim.finished.connect(on_finished)
        anim.finished.connect(lambda: self._remove_anim(anim))
        self.anim_group.addAnimation(anim)
        return anim

    def play(self):
        self.anim_group.start()

    def stop(self):
        self.anim_group.stop()
        self.anim_group.clear()
        self.anims.clear()
        self.check_all_anims_done()

    def _remove_anim(self, anim: QAbstractAnimation) -> None:
        self.anims.remove(anim)
        self.anim_group.removeAnimation(anim)
        self.check_all_anims_done()

    def check_all_anims_done(self) -> None:
        if self.anim_done_callback and not self.anims:
            self.anim_done_callback()

