import anim

from aztec_circle import aztec
from tile_generator import sequence_tile_generator

from PySide6.QtCore import QPointF

import math

class animation(anim.animation):
    def __init__(self, scene: anim.scene) -> None:
        super().__init__("Aztec Circle", "")
        self.tiles_sequence_option = anim.option("Tiles sequence", "The sequence of tiles generated, a sequence of h, v and r.", "r", "", "")
        self.seed_option = anim.option("Random seed", "The seed used in the random number generator.", 1771, 1000, 100000000)
        self.animate_limit_option = anim.option("Animate until generation", "Animate only until this generation.", 60, 1, 100)

        self.add_options([self.tiles_sequence_option, self.seed_option, self.animate_limit_option])

        self.scene = scene
        self.animator: anim.animator = None
        self.loop = True

        self.reset(scene)

    @property
    def tiles_sequence(self) -> str:
        return self.tiles_sequence_option.value

    @property
    def seed(self) -> int:
        return self.seed_option.value

    @property
    def skip_animations(self) -> bool:
        return self.size > self.animate_limit_option.value

    def reset(self, scene: anim.scene):
        self.anim_duration = 1.
        self.size = 1
        self.items = []
        self.new_items = []
        self.show_boundary = False
        self.cross = None
        self.arrow = None
        self.az = aztec(0, sequence_tile_generator(self.seed, self.tiles_sequence), self)
        super().reset(scene)

    def generate_actors(self, scene: anim.scene) -> None:
        self.cross = anim.actor("cross", "", anim.items.create_cross())
        self.cross.item.setZValue(100.)
        self.cross.item.setOpacity(0.)
        self.add_actors(self.cross, scene)

        self.arrow = anim.actor("arrow", "", self.create_arrow_for_tile(None))
        self.arrow.item.setZValue(100.)
        self.arrow.item.setOpacity(0.)
        self.add_actors(self.arrow, scene)

    def generate_shots(self) -> None:
        self._anim_increase_size()
        self._anim_remove_collisions()
        self._anim_move_tiles()
        self._anim_fill_holes()

    def option_changed(self, scene: anim.scene, animator: anim.animator, option: anim.option) -> None:
        if option == self.seed_option or option == self.tiles_sequence_option:
            self.az.tile_generator = sequence_tile_generator(self.seed, self.tiles_sequence)


    #################################################################
    #
    # Actors

    def create_cross(self):
        cross = anim.items.create_cross()
        if self.cross:
            cross.setVisible(self.cross.shown)
        return cross

    tile_arrow_angles = [ [-90., 90.], [0., 180.] ]

    def create_arrow_for_tile(self, tile):
        angle = animation.tile_arrow_angles[tile.is_horizontal][tile.is_positive] if tile else 0.
        arrow = anim.items.create_arrow(angle)
        if self.arrow:
            arrow.setVisible(self.arrow.shown)
        return arrow


    #################################################################
    #
    # Shots

    def _anim_increase_size(self):
        def prep_anim(shot: anim.shot, scene: anim.scene, animator: anim.animator):
            self.az.increase_size()
            self.animator = animator
        self.add_shots(anim.shot("Grow diamond", "", prep_anim))

    def _anim_remove_collisions(self):
        def prep_anim(shot: anim.shot, scene: anim.scene, animator: anim.animator):
            self.az.remove_collisions()
        self.add_shots(anim.shot("Remove collisions", "", prep_anim))

    def _anim_move_tiles(self):
        def prep_anim(shot: anim.shot, scene: anim.scene, animator: anim.animator):
            self.az.move_tiles()
        self.add_shots(anim.shot("Move tiles", "", prep_anim))

    def _anim_fill_holes(self):
        def prep_anim(shot: anim.shot, scene: anim.scene, animator: anim.animator):
            self.az.fill_holes()
        self.add_shots(anim.shot("Fill holes", "", prep_anim))


    #################################################################
    #
    # Aztec circle feedback

    def pos_to_scene(self, x: int, y: int) -> tuple:
        return (x * anim.items.tile_size, y * anim.items.tile_size)

    def middle_pos_to_scene(self, x: int, y: int, tile) -> tuple:
        if tile:
            if tile.is_horizontal:
                x += 0.5
            else:
                y += 0.5
        return (x * anim.items.tile_size, y * anim.items.tile_size)

    tile_colors = [ [anim.items.orange_color, anim.items.red_color], [anim.items.blue_color, anim.items.green_color] ]

    @staticmethod
    def tile_to_color(tile):
        return animation.tile_colors[tile.is_horizontal][tile.is_positive]

    def create_scene_tile(self, x: int, y: int, tile):
        x, y = self.pos_to_scene(x, y)
        width  = 2 * anim.items.tile_size if tile.is_horizontal else anim.items.tile_size
        height = anim.items.tile_size if tile.is_horizontal else 2 * anim.items.tile_size
        item = anim.items.create_rect(x, y, width, height, animation.tile_to_color(tile), 1)
        self.scene.add_item(item)
        return item

    def reallocate(self, az, old_amount: int, new_amount: int):
        skip, self.items, self.new_items = aztec.reallocate_data(old_amount, new_amount, self.items, self.new_items)
        self.center = new_amount // 2

    def increase_size(self, az, origin, size):
        if self.show_boundary:
            coord = anim.items.tile_size * (origin - self.center) - 8
            width = anim.items.tile_size * size * 2 + 16
            if not self.boundary:
                self.boundary = self.scene.addRect(coord, coord, width, width, anim.items.gray_pen)
            else:
                self.boundary.setRect(coord, coord, width, width)
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
        cross = self.create_cross()
        cross.setPos(*self.middle_pos_to_scene(x - center, y - center, tile))
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
            item.setPos(*self.pos_to_scene(x2 - center, y2 - center))
            return

        if self.arrow.shown:
            tile = az.tiles()[x1][y1] if az else None
            arrow = self.create_arrow_for_tile(tile)
            arrow.setPos(*self.middle_pos_to_scene(x1 - center, y1 - center, tile))
            arrow.setOpacity(1.)
            self.scene.add_item(arrow)
            self.animator.animate_value(
                QPointF(*self.middle_pos_to_scene(x1 - center, y1 - center, tile)),
                QPointF(*self.middle_pos_to_scene(x2 - center, y2 - center, tile)),
                self.anim_duration,
                anim.anims.move_item(arrow),
                lambda: self.scene.remove_item(arrow)
            )

        self.animator.animate_value(
            QPointF(*self.pos_to_scene(x1 - center, y1 - center)),
            QPointF(*self.pos_to_scene(x2 - center, y2 - center)),
            self.anim_duration,
            anim.anims.move_item(item)
        )

    def moves_done(self, az):
        self.animator.check_all_anims_done()

    def fill(self, az, x, y, tile):
        center = self.center
        item = self.create_scene_tile(x - center, y - center, tile)
        self.new_items[x][y] = item

        if self.skip_animations:
            item.setOpacity(1.)
            self.animator.animate_value(1., 1., 0.001, anim.anims.reveal_item(item))
        else:
            item.setOpacity(0.)
            self.animator.animate_value(0., 1., self.anim_duration, anim.anims.reveal_item(item))

    def fills_done(self, az):
        self.items, self.new_items = self.new_items, self.items
        self.scene.adjust_view_to_fit()
