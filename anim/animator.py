from .ui.ui import connect_auto_signal, disconnect_auto_signals
from .shot import shot
from .scene import scene

from PySide6.QtCore import QVariantAnimation, QAbstractAnimation, QParallelAnimationGroup, Signal, QObject, Qt


class animation_group(QParallelAnimationGroup):
    """
    Animation group containing animatin sthat runs in parallel.
    """

    current_time_changed = Signal(float)

    def __init__(self, parent = None) -> None:
        super().__init__(parent)

    def updateCurrentTime(self, currentTime: int) -> None:
        super().updateCurrentTime(currentTime)
        self._emit_current_time()

    def setCurrentTime(self, msecs: int) -> None:
        super().setCurrentTime(msecs)
        self._emit_current_time()

    def _emit_current_time(self):
        duration = self.totalDuration()
        if duration:
            value = float(self.currentTime()) / float(duration)
        else:
            value = float(0)
        self.current_time_changed.emit(value)


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

    Since animate() also takes a per-animated-item on_finished callback,
    it is also possible to add new animation items when a given item is done.
    This can be useful if you want to chain animations of different items with
    different durations without having to calculate the exact chain of durations.
    """

    def __init__(self) -> None:
        """
        Creates an animator with the given default anmation duration
        and the optional animation-done callback. This callback is called
        once all animations added in animate() are done.
        """
        super().__init__()
        self.anim_speedup = 1.
        self.queued_anims = set()
        self.anim_group = animation_group()
        self.current_scene = None
        self.current_shot = None
        self.current_animation = None

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
            connect_auto_signal(anim, anim.valueChanged, on_changed)
        self.animate(anim, duration, on_finished)

    def animate(self, anim: QAbstractAnimation, duration, on_finished = None) -> None:
        """
        Add the given animation (QAbstractAnimation) the given scene item.

        A value will be animated from the start_value to the end_value over the given fraction
        of the default animation duration.
        
        The given optional on_changed callback is called every time the value changes during the animation.
        The given optional on_finished is called when the animation ends.

        When all animations that were added are done, the current animation shot_ended is called.
        """
        self.queued_anims.add(anim)
        anim.setDuration(max(1., duration * 1000. / max(0.001, self.anim_speedup)))
        if on_finished:
            connect_auto_signal(anim, anim.finished, on_finished)
        ended = lambda: self._anim_ended(anim)
        connect_auto_signal(anim, anim.finished, ended)
        self.anim_group.addAnimation(anim)

    def _remove_anim(self, anim: QAbstractAnimation) -> None:
        # Note: QParallelAnimationGroup clear deletes the animations,
        #       so we need to remove them before calling it, because
        #       sometimes we are being called within an animation signal
        #       and deleting the animation in that case would crash.
        self.anim_group.removeAnimation(anim)
        disconnect_auto_signals(anim)
        self.queued_anims.remove(anim)

    def _anim_ended(self, anim: QAbstractAnimation) -> None:
        self._remove_anim(anim)
        self.check_all_anims_done()

    def play(self, shot: shot, animation, scene: scene) -> None:
        """
        Sets all previous animation to their end-time, trigger their
        anim-finished signals, removes all these previous animations
        from the anim group, clear all queued animations.

        Prepare all animations of the shot by calling their prepare_anim functions
        unless the shot is set to not be shown, in which case do nothing.
        """
        if not shot.shown:
            return

        # Make sure the anim group is stopped.
        self.stop()

        # Clear the current shot to avoid triggering
        # the shot_ended signal since we are restarting play,
        # we don't want to confuse the caller and potentially
        # cause a double-start.
        self.current_shot = None

        # Make sure all previous animation are at their end-time
        # And their finished signal has been triggered.
        for anim in list(self.queued_anims):
            anim.setCurrentTime(anim.totalDuration())
            anim.finished.emit()

        self.reset()

        self.current_shot = shot
        self.current_scene = scene
        self.current_animation = animation
        for prep in shot.prepare_anims:
            prep(shot, scene, self)
        scene.ensure_all_contents_fit()

        self.anim_group.start()
        self.check_all_anims_done()

    def set_current_time_fraction(self, frac: float):
        """
        Sets the current time of the animation in fraction of the duration,
        between zero and one.
        """
        duration = self.anim_group.totalDuration()
        self.anim_group.setCurrentTime(int(round(duration * frac)))

    def stop(self) -> None:
        """
        Stops the anim group.
        """
        self.anim_group.stop()

    def reset(self):
        """
        Clears all animations without triggering anything.
        """
        for anim in list(self.queued_anims):
            self._remove_anim(anim)
        self.queued_anims.clear()
        self.anim_group.clear()
        self.current_scene = None
        self.current_shot = None
        self.current_animation = None

    def are_all_anims_done(self):
        return not self.queued_anims

    def check_all_anims_done(self) -> None:
        if not self.current_shot:
            return

        if not self.are_all_anims_done():
            return

        # Note: keep a copy of the current shot, scene and animation
        #       and clear them immediately before calling cleanup of
        #       the current shot it may queue a new shot.
        shot = self.current_shot
        scene = self.current_scene
        animation = self.current_animation
        self.current_shot = None
        self.current_scene = None
        self.current_animation = None

        for cleanup in shot.cleanup_anims:
            cleanup(shot, scene, self)

        # If the cleanup queued more animations, keep playing them.
        if not self.are_all_anims_done():
            return

        if animation:
            animation.shot_ended(shot, scene, self)


