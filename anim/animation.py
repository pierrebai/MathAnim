from .actor import actor
from .animator import animator
from .shot import shot
from .options import option, options
from .scene import scene
from . import anims

from collections import defaultdict
from typing import Dict, List

from PySide6.QtCore import QPointF, Signal, QObject


class animation(QObject):

    on_shot_changed = Signal(scene, animator, shot)

    def __init__(self, name: str, description: str, scene: scene, animator: animator) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.options = options()
        self.actors = set()
        self.shots = []
        self.current_shot_index = -1
        self.loop = False
        self.playing = False

        self.anim_speed_option = option("Animation speed", "How fast the animations is played.", int(animator.anim_speedup * 20), 1, 100)
        self.add_options(self.anim_speed_option)

        animator.shot_ended.connect(self._shot_ended)

    def reset(self, scene: scene, animator: animator) -> None:
        """
        Clears the actors and shots and recreates them.
        """
        was_last = (self.current_shot_index == len(self.shots) - 1)
        shown_by_names = self.get_shown_actors_by_names()

        for actor in self.actors:
            scene.remove_actor(actor)
        scene.remove_all_items()
        self.actors = set()
        self.shots = []

        animator.stop()
        animator.reset()
        
        self.generate_actors(scene)
        self.actors.add(scene.pointing_arrow)
        self.apply_shown_to_actors(shown_by_names)
        self.generate_shots()
        scene.ensure_all_contents_fit()

        if was_last:
            self.current_shot_index = len(self.shots) - 1
        else:
            self.current_shot_index = 0
        scene.set_title(self.shots[self.current_shot_index].name)
        scene.set_description(self.shots[self.current_shot_index].description)

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

    def _handle_speed_options(self, scene: scene, animator: animator, option: option) -> None:
        """
        Handles the animation speed option, which all animations get.
        """
        if option == self.anim_speed_option:
            animator.anim_speedup = int(option.value) / 20.

    def option_changed(self, scene: scene, animator: animator, option: option) -> None:
        """
        Called when an option value is changed. By default it resets the animation
        (calls reset) and continue the animation with the new settings.
        
        Override in sub-classes to react to option changes.
        """
        # The reset function regenerate the actors, anims and shots,
        # which will make the animator pick up the new animations on the fly.
        self._handle_speed_options(scene, animator, option)
        self.reset(scene, animator)
        self.resume_play(scene, animator)

    def anim_pointing_arrow(self, head_point: QPointF, duration: float, scene: scene, animator: animator):
        """
        Animate the pointing arrow to point to the new point of interest.
        """
        tail_pos = QPointF(scene.pointing_arrow.item.tail)
        desc_rect = scene.descriptionBox.sceneBoundingRect()
        desc_pos = desc_rect.topLeft()
        animator.animate_value(tail_pos, desc_pos, duration, anims.move_point(scene.pointing_arrow.item.tail))

        head_pos = QPointF(scene.pointing_arrow.item.head)
        what_pos = QPointF(head_point)
        animator.animate_value(head_pos, what_pos, duration, anims.move_point(scene.pointing_arrow.item.head))

    def play(self, scene: scene, animator: animator, start_at_shot_index = None) -> None:
        if self.playing:
            return
        self.playing = True
        self.single_shot = False
        if not start_at_shot_index is None:
            self.current_shot_index = start_at_shot_index - 1
        self.play_next_shot(scene, animator)

    def play_all(self, scene: scene, animator: animator) -> None:
        self.play(scene, animator)

    def play_next_shot(self, scene: scene, animator: animator) -> None:
        self.current_shot_index = self.current_shot_index + 1
        self.play_current_shot(scene, animator)

    def play_current_shot(self, scene: scene, animator: animator) -> None:
        if not self.shots:
            return

        if not self.playing:
            self.single_shot = True

        self.resume_play(scene, animator)

    def resume_play(self, scene: scene, animator: animator) -> None:
        if not self.playing:
            self.playing = True

        self.current_shot_index = self.current_shot_index % len(self.shots)
        current_shot = self.shots[self.current_shot_index]
        scene.set_title(current_shot.name)
        scene.set_description(current_shot.description)
        animator.play(current_shot, scene)
        self.on_shot_changed.emit(scene, animator, current_shot)

    def _shot_ended(self, ended_shot: shot, ended_scene: scene, ended_animator: animator):
        if not self.playing or self.single_shot or (not self.loop and not ended_shot.repeat and self.current_shot_index == len(self.shots) - 1):
            self.stop(ended_scene, ended_animator)
        elif ended_shot.repeat:
            self.play_current_shot(ended_scene, ended_animator)
        else:
            self.play_next_shot(ended_scene, ended_animator)

    def stop(self, scene: scene, animator: animator) -> None:
        if not self.playing:
            return
        self.playing = False
        animator.stop()
