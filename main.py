import anim
import anim.ui.app_window

from examples.aztec_circle.animation import animation as aztec_circle
from examples.rotating_stars.animation import animation as rotating_stars

app = anim.ui.create_app()
scene = anim.scene()
animator = anim.animator()
anims = [
    ("Aztec Circle", aztec_circle),
    ("Rotating Stars", rotating_stars),
]
window = anim.ui.app_window.create_app_window(anims, scene, animator)

anim.ui.start_app(app, window)

