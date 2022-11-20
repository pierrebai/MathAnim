import anim.ui
import anim.ui.app_window

app = anim.ui.create_app()

from examples.aztec_circle.aztec_circle import aztec_circle
from examples.rotating_stars.rotating_stars import rotating_stars
from examples.quarter_geometric_sum.quarter_geometric_sum import quarter_geometric_sum
from examples.vortex_maths.vortex_maths import vortex_maths
from examples.three_bisectors.three_bisectors import three_bisectors
from examples.pentagramaths.pentagramaths import pentagramaths
from examples.lonely_runner.lonely_runner import lonely_runner

anims = [
    lonely_runner,
    pentagramaths,
    three_bisectors,
    vortex_maths,
    quarter_geometric_sum,
    aztec_circle,
    rotating_stars,
]

window = anim.ui.app_window.create_app_window(anims)

anim.ui.start_app(app, window)

