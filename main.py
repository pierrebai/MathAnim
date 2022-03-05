import anim.ui
import anim.ui.app_window

app = anim.ui.create_app()

from examples.aztec_circle.animation import animation as aztec_circle
from examples.rotating_stars.animation import animation as rotating_stars
from examples.quarter_geometric_sum.animation import animation as quarter_geometric_sum
from examples.vortex_maths.animation import animation as vortex_maths
from examples.three_bisectors.animation import animation as three_bisectors

anims = [
    three_bisectors,
    vortex_maths,
    quarter_geometric_sum,
    aztec_circle,
    rotating_stars,
]

window = anim.ui.app_window.create_app_window(anims)

anim.ui.start_app(app, window)

