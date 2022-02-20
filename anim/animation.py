from anim.items.point import static_point, point
from .actor import actor
from .animator import animator
from .named import named
from .shot import shot
from .options import option, options
from .scene import scene
from . import anims

from collections import defaultdict
from typing import Dict, List

from PySide6.QtCore import QPointF, Signal, QObject


class animation(QObject, named):
    """
    Animation base class.

    To create an animation, derive from this and implement the following functions:

        - reset(): resets the animation. Calls generate_actors and generate_shots again.
                   The reset function gets called when the options of the animation change
                   or when the user press the reset-button in the UI.

                   The reset() function must be called before using the animation.
                   The app window automatically calls it when a new animation is
                   selected.

        - generate_actors(scene): generates the actors that will be used in the
                                  animation. The names of the actors will be used
                                  to create UI to let the user decide what gets drawn.

                                  All actors must be added to the animation by calling
                                  the add_actors function from within generate_actors,
                                  passng the actors and the scene.

        - generate_shots(): generates the shots that make=up the entire animation.

                            All shots must be added to the animation by calling the
                            add_shots function from within generate_shots, passing
                            the shots.

                            A shot has a name, description and at least a prepare_anim
                            function. Optionally, it can have a cleanup_anim function.

                            The prepare_anim function of each shot receives the shot,
                            scene and animator. It must registers animations to be
                            played by calling the animate_value function of the animator,
                            possibly multiple times, for all the actors that will
                            participate in the shot.

        - option_changed(): called when an option has changed. Normally you can simply
                            implement reset() or even just let the generate_actors and
                            generate_shots react to the new options.

        - shot_ended(): called when the currently playing shot ends. By default, plays
                        the next shot if the animation is still playing.
    """
    def __init__(self, name: str, description: str) -> None:
        QObject.__init__(self)
        named.__init__(self, name, description)
        self.name = name
        self.description = description

        self.options = options()
        self.actors = set()
        self.shots = []

        self.current_shot_index = -1
        self.playing = False

        self.loop = False
        self.reset_on_change = True

        self.anim_speed_option = option("Animation speed", "How fast the animations is played.", 20, 1, 100)
        self.add_options(self.anim_speed_option)


    on_shot_changed = Signal(scene, animator, shot)


    ########################################################################
    #
    # Overridable functions
    
    def reset(self, scene: scene, animator: animator) -> None:
        """
        Clears the actors and shots and recreates them by calling
        the generate_actors and generate_shots functions.

        The reset function gets called when the options of the animation
        change or when the user press the reset-button in the UI.
        """
        was_last = (self.current_shot_index >= 0 and self.current_shot_index == len(self.shots) - 1)
        shown_by_names = self.get_shown_actors_by_names()

        animator.reset()
        
        for actor in self.actors:
            scene.remove_actor(actor)
        scene.remove_all_items()
        self.actors = set()
        self.shots = []

        self.generate_actors(scene)
        self.actors.add(scene.pointing_arrow)
        self.apply_shown_to_actors(shown_by_names)
        self.generate_shots()
        scene.ensure_all_contents_fit()

        if was_last:
            self.current_shot_index = len(self.shots) - 1
        else:
            self.current_shot_index = -1

    def generate_actors(self, scene: scene) -> None:
        """
        Generates the actors that will be used in the animation.

        The names of the actors will be used to create UI to let
        the user decide what gets drawn.

        All actors must be added to the animation by calling
        the add_actors function from within generate_actors,
        passng the actors and the scene.
        """
        pass

    def generate_shots(self) -> None:
        """
        Generates the shots that make=up the entire animation.

        All shots must be added to the animation by calling the
        add_shots function from within generate_shots, passing
        the shots.

        A shot has a name, description and at least a prepare_anim
        function. Optionally, it can have a cleanup_anim function.

        The prepare_anim function of each shot receives the shot,
        scene and animator. It must registers animations to be
        played by calling the animate_value function of the animator,
        possibly multiple times, for all the actors that will
        participate in the shot.
        """
        pass

    def option_changed(self, scene: scene, animator: animator, option: option) -> None:
        """
        Called when an option value is changed. The base class handles
        change to the animation-speed option.
        
        If the reset_on_change flag is True then it calls the
        reset function and continues playing the animation with the new
        settings.
        
        Override in sub-classes to react to option changes, if needed.
        You can instead react to the options in reset() or just let the
        generate_actors and generate_shots functions react to the new
        options when they do their work.
        """
        self._handle_speed_options(scene, animator, option)

        if self.reset_on_change:
            # The reset function regenerate the actors, anims and shots,
            # which will make the animator pick up the new animations on the fly.
            was_playing = self.playing
            self.reset(scene, animator)
            self.resume_play(scene, animator)
            if not was_playing:
                self.stop(scene, animator)

    def shot_ended(self, ended_shot: shot, ended_scene: scene, ended_animator: animator):
        """
        Called when the current shot has finished playing in the animator.
        """
        is_last_shot = (self.current_shot_index == len(self.shots) - 1)
        has_more_shots = self.loop or ended_shot.repeat or not is_last_shot
        keep_playing = self.playing and not self.single_shot and has_more_shots
        if not keep_playing:
            self.stop(ended_scene, ended_animator)
        elif ended_shot.repeat:
            self.play_current_shot(ended_scene, ended_animator)
        else:
            self.play_next_shot(ended_scene, ended_animator)


    ########################################################################
    #
    # Actors

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

    def get_actors_by_names(self) -> Dict[str, List[actor]]:
        """
        Returns a dict of actor lists indexed by the actor name.
        """
        actors_by_names = defaultdict(list)
        for actor in self.actors:
            actors_by_names[actor.name].append(actor)
        return actors_by_names

    def get_shown_actors_by_names(self) -> Dict[str, bool]:
        """
        Returns a dict of shown / not shown flags indexed by actor names.
        """
        return {
            name: actors[0].shown for name, actors in self.get_actors_by_names().items()
        }

    def apply_shown_to_actors(self, shown_by_names: Dict[str, bool]) -> None:
        """
        Applies a preserved shown actors dictionary on the given animation actors.
        """
        for actor in self.actors:
            if actor.name in shown_by_names:
                actor.show(shown_by_names[actor.name])


    ########################################################################
    #
    # Shots

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

    def place_anim_pointing_arrow(self, head_point: static_point, scene: scene):
        """
        Place the pointing arrow to start at the description and
        point to the given point.
        """
        desc_rect = scene.description_box.sceneBoundingRect()
        desc_pos = desc_rect.topLeft()
        scene.pointing_arrow.item.tail.set_point(desc_pos)
        scene.pointing_arrow.item.head.set_point(head_point)

    def anim_pointing_arrow(self, head_point: static_point, duration: float, scene: scene, animator: animator):
        """
        Animate the pointing arrow to point to the new point of interest.
        Used in shots created by the sub-classes.
        """
        tail_pos = QPointF(scene.pointing_arrow.item.tail)
        desc_rect = scene.description_box.sceneBoundingRect()
        desc_pos = desc_rect.topLeft()
        animator.animate_value(tail_pos, desc_pos, duration, anims.move_point(scene.pointing_arrow.item.tail))

        head_pos = QPointF(scene.pointing_arrow.item.head)
        what_pos = QPointF(head_point)
        animator.animate_value(head_pos, what_pos, duration, anims.move_point(scene.pointing_arrow.item.head))


    ########################################################################
    #
    # Options

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

    def _handle_speed_options(self, scene: scene, animator: animator, option: option) -> None:
        """
        Handles the animation speed option, which all animations get.
        """
        if option == self.anim_speed_option:
            animator.anim_speedup = int(option.value) / 20.


    ########################################################################
    #
    # Play / Stop / etc

    def play(self, scene: scene, animator: animator, start_at_shot_index = None) -> None:
        """
        Starts to play all shots if not already playing.

        If already playing, does nothing.
        """
        if self.playing:
            return
        self.playing = True
        self.single_shot = False
        if not start_at_shot_index is None:
            self.current_shot_index = start_at_shot_index - 1
        self.play_next_shot(scene, animator)

    def play_next_shot(self, scene: scene, animator: animator) -> None:
        """
        Plays the next shot, even if already playing.

        If the current shot is a repeating shot, then this repeats the
        curent shot.
        """
        current_shot = self.shots[self.current_shot_index]
        if self.current_shot_index == -1 or not current_shot.repeat:
            self.current_shot_index = self.current_shot_index + 1
        self.play_current_shot(scene, animator)

    def play_current_shot(self, scene: scene, animator: animator) -> None:
        """
        If it was already playing, plays the current shot and keep playing.
        If it was not already playing, then play *only* the current shot.
        """
        if not self.shots:
            return

        if not self.playing:
            self.single_shot = True

        self.resume_play(scene, animator)

    def resume_play(self, scene: scene, animator: animator) -> None:
        """
        Resume playing if it was already playing, else does nothing.
        """
        if not self.playing:
            self.playing = True

        self.current_shot_index = max(0, self.current_shot_index) % len(self.shots)
        current_shot = self.shots[self.current_shot_index]
        scene.set_title(current_shot.name)
        scene.set_description(current_shot.description)
        animator.play(current_shot, self, scene)
        self.on_shot_changed.emit(scene, animator, current_shot)

    def stop(self, scene: scene, animator: animator) -> None:
        """
        Stops playing. Does nothing if already stopped.
        """
        if not self.playing:
            return
        self.playing = False
        animator.stop()
