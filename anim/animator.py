from PyQt5.QtCore import QVariant, QVariantAnimation, QPointF

import math


class animator:
    """
    Animate items over the anim_duration time. This is a single animation shot.
    
    This can be repeated over and over to create a sequence of animations,
    creating a shot-by-shot demonstration.

    The actual animation duration can be shorter or longer that the given
    anim_duration. That duration is only used as a baseline default duration.
    When items are animated, a duration fraction can be given that scales
    the default duration. A fraction below 1 is shorter, a fraction over one
    is longer. So to get a single animation can be made 3x longer than the
    default by giving 3 as the animation fraction in add_anim().

    The typical usage is to given a anim_done_callback when creating the
    animator that sets up the next animation shot. In each animation shot,
    add_anim() is called multiple times to specify which item gets animated.

    Since add_anim() also takes a per-animated-item on_finished callback,
    it is also possible to add new animation items when a given item is done.
    This can be useful if you want to chain animations of different items with
    different durations without having to calculate the exact chain of durations.
    """

    def __init__(self, anim_duration, anim_done_callback, *args, **kwargs):
        """
        Creates an animator with the given default anmation duration
        and the optional animation-done callback. This callback is called
        once all animations added in add_anim() are done.
        """
        super(animator, self).__init__(*args, **kwargs)
        self.anim_done_callback = anim_done_callback
        self.anim_duration = anim_duration
        self.anim_duration_speedup = 1.
        self.anims = set()


    #################################################################
    #
    # Animations

    def add_anim(self, item, start_value, end_value, on_changed, on_finished, duration_fraction = 1.):
        """
        Animate the given scene item.

        A value will be animated from the start_value to the end_value over the given fraction
        of the default animation duration.
        
        The given optional on_changed callback is called every time the value changes during the animation.
        The given optional on_finished is called when the animation ends.

        When all animations that were added are done, the class anim_done_callback is called.
        """
        anim = QVariantAnimation()
        self.anims.add(anim)
        anim.setDuration(max(1., self.anim_duration * duration_fraction * self.anim_duration_speedup))
        anim.setStartValue(QVariant(start_value))
        anim.setEndValue(QVariant(end_value))
        if on_changed:
            anim.valueChanged.connect(on_changed)
        if on_finished:
            anim.finished.connect(on_finished)
        anim.finished.connect(lambda: self._remove_anim(anim))
        anim.start()
        return anim

    def _remove_anim(self, anim):
        self.anims.remove(anim)
        self._check_all_anims_done()

    def _check_all_anims_done(self):
        if self.anim_done_callback and not self.anims:
            self.anim_done_callback()

