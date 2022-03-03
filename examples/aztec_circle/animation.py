import anim

from .aztec_circle import aztec
from .tile_generator import sequence_tile_generator

import math

class animation(anim.animation):
    def __init__(self) -> None:
        super().__init__("Aztec Circle", "Aztec artic circle tiling, as per the Mathologer you-tube video.")
        
        self.tiles_sequence_option = anim.option("Tiles sequence", "The sequence of tiles generated, a sequence of h, v and r.", "r", "", "")
        self.seed_option = anim.option("Random seed", "The seed used in the random number generator.", 1771, 1000, 100000000)
        self.animate_limit_option = anim.option("Animate until generation", "Animate only until this generation.", 60, 1, 100)

        self.loop = True
        self.reset_on_change = False

        self.scene: anim.scene = None
        self.animator: anim.animator = None

    def reset(self, scene: anim.scene, animator: anim.animator):
        self.scene: anim.scene = scene
        scene.view.set_margin(anim.tile_size)
        self.animator: anim.animator = animator
        self.anim_duration = 1.
        self.size = 1
        self.items = []
        self.new_items = []
        self.cross = None
        self.arrow = None
        self.az = aztec(0, sequence_tile_generator(self.seed, self.tiles_sequence), self)
        super().reset(scene, animator)
        self.remove_pointing_arrow(scene)


    ########################################################################
    #
    # Options.

    @property
    def tiles_sequence(self) -> str:
        return self.tiles_sequence_option.value

    @property
    def seed(self) -> int:
        return self.seed_option.value

    @property
    def skip_animations(self) -> bool:
        return self.size > self.animate_limit_option.value

    def option_changed(self, scene: anim.scene, animator: anim.animator, option: anim.option) -> None:
        """
        Called when an option value is changed.
        Override base-class behavior to not interrupt the animations.
        """
        super().option_changed(scene, animator, option)
        self._handle_generator_options(scene, animator, option)

    def _handle_generator_options(self, scene: anim.scene, animator: anim.animator, option: anim.option) -> None:
        if option == self.seed_option or option == self.tiles_sequence_option:
            self.az.tile_generator = sequence_tile_generator(self.seed, self.tiles_sequence)


    #################################################################
    #
    # Actors

    def generate_actors(self, scene: anim.scene) -> None:
        self.cross = anim.actor("cross", "Cross marking a tile about to be deleted", anim.create_cross(anim.point()).set_opacity(0))
        self.add_actors(self.cross, scene)

        self.arrow = anim.actor("arrow", "Arrow marking the direction a tile is moving", self.create_arrow_for_tile(anim.point(0., 0.), None).set_opacity(0.))
        self.add_actors(self.arrow, scene)

        self.boundary = anim.actor("boundary", "The boundary of the growing diamond", anim.create_rect(0., 0., 1., 1.).outline(anim.gray).thickness(1.).fill(anim.no_color))
        self.boundary.show(False)
        self.add_actors(self.boundary, scene)

    def create_cross(self, origin):
        cross = anim.create_cross(origin)
        if self.cross:
            cross.set_shown(self.cross.shown)
        return cross

    _tile_arrow_angles = [ [-90., 90.], [0., 180.] ]
    @staticmethod
    def tile_to_angle(tile) -> float:
        return animation._tile_arrow_angles[tile.is_horizontal][tile.is_positive] if tile else 0.

    tile_colors = [ [anim.orange, anim.red], [anim.blue, anim.green] ]

    @staticmethod
    def tile_to_color(tile):
        return animation.tile_colors[tile.is_horizontal][tile.is_positive]

    def create_arrow_for_tile(self, origin, tile):
        arrow = anim.create_arrow(origin, animation.tile_to_angle(tile))
        if self.arrow:
            arrow.set_shown(self.arrow.shown)
        return arrow

    def create_scene_tile(self, x: int, y: int, tile):
        p1 = self.pos_to_scene(x, y)
        width  = 2 * anim.tile_size if tile.is_horizontal else anim.tile_size
        height = anim.tile_size if tile.is_horizontal else 2 * anim.tile_size
        p2 = anim.relative_point(p1, width, height)
        item = anim.create_two_points_rect(p1, p2).fill(animation.tile_to_color(tile)).thickness(1)
        self.scene.add_item(item)
        return item


    #################################################################
    #
    # Shots

    def generate_shots(self) -> None:
        self._anim_increase_size()
        self._anim_remove_collisions()
        self._anim_move_tiles()
        self._anim_fill_holes()

    def _anim_increase_size(self):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            self.az.increase_size()
        self.add_shots(anim.shot(
            "Grow diamond",
            "Prepare the diamond\n"
            "to grow by increasing\n"
            "the imaginary boundary\n"
            "inside which it is drawn.",
            prep_anim))

    def _anim_remove_collisions(self):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            self.az.remove_collisions()
        self.add_shots(anim.shot(
            "Remove collisions",
            "Mark and remove the tiles\n"
            "that will collide when moved.",
            prep_anim))

    def _anim_move_tiles(self):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            self.az.move_tiles()
        self.add_shots(anim.shot(
            "Move tiles",
            "Move all remaining tiles\n"
            "in the direction matching\n"
            "their tile color.",
            prep_anim))

    def _anim_fill_holes(self):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            self.az.fill_holes()
        self.add_shots(anim.shot(
            "Fill holes",
            "Fill the holes created by\n"
            "the moved tiles with new\n"
            "tiles generated randomly\n"
            "following the recipe you\n"
            "give in the tiles sequence.",
            prep_anim))


    #################################################################
    #
    # Aztec circle feedback

    def pos_to_scene(self, x: int, y: int) -> anim.point:
        return anim.point(x * anim.tile_size, y * anim.tile_size)

    def middle_pos_to_scene(self, x: int, y: int, tile) -> tuple:
        if tile:
            if tile.is_horizontal:
                x += 1
                y += 0.5
            else:
                x += 0.5
                y += 1
        return (x * anim.tile_size, y * anim.tile_size)

    def reallocate(self, az, old_amount: int, new_amount: int):
        skip, self.items, self.new_items = aztec.reallocate_data(old_amount, new_amount, self.items, self.new_items)
        self.center = new_amount // 2

    def increase_size(self, az, origin, size):
        coord = anim.tile_size * (origin - self.center) - 8
        width = anim.tile_size * size * 2 + 16
        self.boundary.item.setRect(coord, coord, width, width)
        self.size = size
        self.anim_duration = 1. / math.sqrt(size / 4)

    def collision(self, az, x, y):
        if self.skip_animations:
            item = self.items[x][y]
            if item:
                self.scene.remove_item(item)
            return

        center = self.center
        tile = az.tiles()[x][y] if az else None
        origin = anim.point(*self.middle_pos_to_scene(x - center, y - center, tile))
        cross = self.create_cross(origin)
        self.scene.add_item(cross)

        item = self.items[x][y]
        if not item:
            return

        self.animator.animate_value(0., 1., self.anim_duration,
            anim.anims.reveal_item(cross),
            lambda: self.scene.remove_item(cross))

        self.animator.animate_value(1., 0.5, self.anim_duration,
            anim.anims.reveal_item(item),
            lambda: self.scene.remove_item(item))

    def collisions_done(self, az):
        self.animator.check_all_anims_done()

    def move(self, az, x1, y1, x2, y2):
        center = self.center
        item = self.items[x1][y1]
        if not item:
            return
        self.new_items[x2][y2] = item

        if self.skip_animations:
            item.p1.set_point(self.pos_to_scene(x2 - center, y2 - center))
            return

        if self.arrow.shown:
            tile = az.tiles()[x1][y1] if az else None
            origin = anim.point(*self.middle_pos_to_scene(x1 - center, y1 - center, tile))
            arrow = self.create_arrow_for_tile(origin, tile)
            arrow.set_opacity(1.)
            self.scene.add_item(arrow)
            self.animator.animate_value(
                anim.static_point(*self.middle_pos_to_scene(x1 - center, y1 - center, tile)),
                anim.static_point(*self.middle_pos_to_scene(x2 - center, y2 - center, tile)),
                self.anim_duration,
                anim.anims.move_point(origin),
                lambda: self.scene.remove_item(arrow)
            )

        self.animator.animate_value(
            anim.static_point(self.pos_to_scene(x1 - center, y1 - center)),
            anim.static_point(self.pos_to_scene(x2 - center, y2 - center)),
            self.anim_duration,
            anim.anims.move_point(item.p1)
        )

        tile = az.tiles()[x2][y2] if az else None

    def moves_done(self, az):
        self.animator.check_all_anims_done()
        self.scene.ensure_all_contents_fit()

    def fill(self, az, x, y, tile):
        center = self.center
        item = self.create_scene_tile(x - center, y - center, tile)
        self.new_items[x][y] = item

        if self.skip_animations:
            item.set_opacity(1.)
            self.animator.animate_value(1., 1., 0.001, anim.anims.reveal_item(item))
        else:
            item.set_opacity(0.)
            self.animator.animate_value(0., 1., self.anim_duration, anim.anims.reveal_item(item))

    def fills_done(self, az):
        self.items, self.new_items = self.new_items, self.items
        self.scene.ensure_all_contents_fit()
