import anim.ui
import anim.ui.app_window

from examples.aztec_circle.animation import animation as aztec_circle
from examples.rotating_stars.animation import animation as rotating_stars
from examples.quarter_geometric_sum.animation import animation as quarter_geometric_sum

anims = [
    aztec_circle,
    rotating_stars,
    quarter_geometric_sum,
]

app = anim.ui.create_app()
window = anim.ui.app_window.create_app_window(anims)

anim.ui.start_app(app, window)

