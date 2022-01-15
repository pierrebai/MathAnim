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

        self.generator = sequence_tile_generator(7, "r")

        self.reset(scene)

    @property
    def tiles_sequence(self) -> str:
        return self.tiles_sequence_option.value

    @property
    def seed(self) -> int:
        return self.seed_option.value

    @property
    def skip_animations(self) -> bool:
        return self.size > 60 # TODO: add option

    def reset(self, scene: anim.scene):
        self.scene = scene
        self.animator: anim.animator = None
        self.anim_duration_speedup = 1.
        self.size = 1
        self.items = []
        self.new_items = []
        self.show_boundary = False
        self.generator.reset()
        self.az = aztec(0, self.generator, self)
        super().reset(scene)

    def generate_actors(self, scene: anim.scene) -> None:
        self.cross = anim.actor("cross", "", anim.items.create_cross())
        self.cross.item.setZValue(100.)
        self.cross.item.setOpacity(0.)
        self.add_actors(self.cross, scene)

        self.arrows_for_tiles = [
            [ anim.actor("arrow", "", anim.items.create_arrow(-90.)), anim.actor("arrow", "", anim.items.create_arrow(90.)) ],
            [ anim.actor("arrow", "", anim.items.create_arrow(0.)), anim.actor("arrow", "", anim.items.create_arrow(180.)) ],
        ]
        for arrows in self.arrows_for_tiles:
            for arrow in arrows:
                arrow.item.setZValue(100.)
                arrow.item.setOpacity(0.)
        self.add_actors(self.arrows_for_tiles, scene)

    def generate_shots(self) -> None:
        #self._anim_intial_circle()
        self._anim_increase_size()
        self._anim_remove_collisions()
        self._anim_move_tiles()
        self._anim_fill_holes()


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
        
        def cleanup_anim(shot: anim.shot, scene: anim.scene, animator: anim.animator):
            if self.playing:
                self.play_all(scene, animator)

        self.add_shots(anim.shot("Fill holes", "", prep_anim, cleanup_anim))


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
        self.add_actors(anim.actor("Tile", "", item), self.scene)
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
        self.anim_duration_speedup = 1. / math.sqrt(size / 4)

    def collision(self, az, x, y):
        center = self.center
        tile = az.tiles()[x][y] if az else None
        self.cross.item.setPos(*self.middle_pos_to_scene(x - center, y - center, tile))

        item = self.items[x][y]

        self.animator.animate_value(1., 0., self.anim_duration_speedup,
            anim.anims.reveal_item(self.cross),
            lambda: self._collision_anim_done(item))

    def _collision_anim_done(self, item):
        self.scene.scene.removeItem(item)

    def collisions_done(self, az):
        self.animator.check_all_anims_done()

    def tile_to_arrow(self, tile):
        return self.arrows_for_tiles[tile.is_horizontal][tile.is_positive] if tile else None

    def move(self, az, x1, y1, x2, y2):
        if self.skip_animations:
            center = self.center
            item = self.items[x1][y1]
            item.setPos(*self.pos_to_scene(x2 - center, y2 - center))
            self.new_items[x2][y2] = item

        center = self.center
        tile = az.tiles()[x1][y1] if az else None
        arrow = self.tile_to_arrow(tile)
        if arrow and arrow.shown:
            arrow.item.setPos(*self.middle_pos_to_scene(x1 - center, y1 - center, tile))
            arrow.item.setOpacity(1.)
            self.animator.animate_value(
                QPointF(*self.middle_pos_to_scene(x1 - center, y1 - center, tile)),
                QPointF(*self.middle_pos_to_scene(x2 - center, y2 - center, tile)),
                self.anim_duration_speedup,
                anim.anims.move_item(arrow.item),
                lambda: arrow.item.setOpacity(0.)
            )

        item = self.items[x1][y1]
        if not item:
            raise Exception()
        self.new_items[x2][y2] = item
        self.animator.animate_value(
            QPointF(*self.pos_to_scene(x1 - center, y1 - center)),
            QPointF(*self.pos_to_scene(x2 - center, y2 - center)),
            self.anim_duration_speedup,
            anim.anims.move_item(item)
        )

    def moves_done(self, az):
        self.animator.check_all_anims_done()

    def fill(self, az, x, y, tile):
        center = self.center
        item = self.create_scene_tile(x - center, y - center, tile)
        self.new_items[x][y] = item

        if self.skip_animations:
            return

        item.setOpacity(0.)
        self.animator.animate_value(0., 1., self.anim_duration_speedup, anim.anims.reveal_item(item))

    def fills_done(self, az):
        self.items, self.new_items = self.new_items, self.items
        self.scene.adjust_view_to_fit()
