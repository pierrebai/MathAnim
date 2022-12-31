from .ui.ui import connect_auto_signal, disconnect_auto_signals
from .shot import shot
from .scene import scene
from .items import static_point

from PySide6.QtCore import QVariantAnimation, QAbstractAnimation, QParallelAnimationGroup, Signal, QObject, Qt, QPointF

from typing import List as _List

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
        self.ended_anims = set()
        self.anim_group = animation_group()
        self.current_scene = None
        self.current_shot = None
        self.current_animation = None

    #################################################################
    #
    # Animations

    def animate_value(self, values: _List, duration: float, on_changed = None, on_finished = None) -> None:
        """
        Animate the given scene item value.

        A value will be animated from the start_value to the end_value over
        the given animation duration, in seconds.
        
        The given optional on_changed callback is called every time the value changes during the animation.
        The given optional on_finished is called when the animation ends.

        When all animations that were added are done, the current animation shot_ended function is called.
        """
        if not values:
            return
        count = len(values)
        if count >= 2:
            timed_values = [(i / float(count - 1), values[i]) for i in range(count)]
        else:
            timed_values[0., values[0]]
        self.animate_timed_value(timed_values, duration, on_changed, on_finished)

    def animate_timed_value(self, values: _List, duration: float, on_changed = None, on_finished = None) -> None:
        """
        Animate the given scene item value.

        A value will be animated from the start_value to the end_value over
        the given animation duration, in seconds.
        
        The given optional on_changed callback is called every time the value changes during the animation.
        The given optional on_finished is called when the animation ends.

        When all animations that were added are done, the current animation shot_ended function is called.
        """
        if not values:
            return

        anim = QVariantAnimation()

        anim.setStartValue(values[0][1])
        anim.setEndValue(values[-1][1])
        anim.setKeyValues(values)
        if on_changed:
            connect_auto_signal(anim, anim.valueChanged, on_changed)
        self.animate(anim, duration, on_finished)

    def animate(self, anim: QAbstractAnimation, duration: float, on_finished = None) -> None:
        """
        Add the given animation (QAbstractAnimation) the given scene item
        with the given animation duration, in seconds.

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

    def _remove_all_anims(self) -> None:
        # Note: QParallelAnimationGroup clear deletes the animations,
        #       so we need to remove them before calling it, because
        #       sometimes we are being called within an animation signal
        #       and deleting the animation in that case would crash.
        for anim in list(self.queued_anims):
            self.anim_group.removeAnimation(anim)
            disconnect_auto_signals(anim)
            self.queued_anims.remove(anim)

    def _anim_ended(self, anim: QAbstractAnimation) -> None:
        self.ended_anims.add(anim)
        self.check_all_anims_done()

    def play(self, shot: shot, animation, scene: scene) -> None:
        """
        Sets all previous animation to their end-time, trigger their
        anim-finished signals, removes all these previous animations
        from the anim group, clear all queued animations.

        Prepare all animations of the shot by calling their prepare_anim functions
        unless the shot is set to not be shown, in which case do nothing.
        """
        # Make sure the anim group is stopped and everything
        # from a previous shot is cleared.
        self.reset()

        # if the shot is not shown, trigger the shot_ended and return.
        if not shot.shown:
            if animation:
                animation.shot_ended(shot, scene, self)
            return

        self.current_shot = shot
        self.current_scene = scene
        self.current_animation = animation
        shot.prepare(animation, scene, self)
        scene.ensure_all_contents_fit()

        self.anim_group.start()
        self.check_all_anims_done()

    def stop(self) -> None:
        """
        Stops the anim group.
        """
        self.anim_group.stop()

    def set_current_time_fraction(self, frac: float):
        """
        Sets the current time of the animation in fraction of the duration,
        between zero and one.
        """
        duration = self.anim_group.totalDuration()
        self.anim_group.setCurrentTime(int(round(duration * frac)))

    def reset(self):
        """
        Clears all animations without triggering anything.
        """
        # Stop the animation before removing its elements.
        self.stop()

        self.current_scene = None
        self.current_shot = None
        self.current_animation = None

        # Make sure all previous animation are at their end-time
        # And their finished signal has been triggered.
        for anim in list(self.queued_anims):
            anim.setCurrentTime(anim.totalDuration())
            if not anim in self.ended_anims:
                anim.finished.emit()

        self._remove_all_anims()

        self.queued_anims.clear()
        self.ended_anims.clear()
        self.anim_group.clear()

    def are_all_anims_done(self):
        return len(self.queued_anims) == len(self.ended_anims)

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

        shot.cleanup(animation, scene, self)

        # If the cleanup queued more animations, keep playing them.
        if not self.are_all_anims_done():
            return

        if animation:
            animation.shot_ended(shot, scene, self)


