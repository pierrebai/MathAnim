import animation
import anim
import anim.ui.app_window

app = anim.ui.create_app()
scene = anim.scene()
animator = anim.animator()
the_anim = animation.animation(scene, animator)
window = anim.ui.app_window.create_app_window(the_anim, scene, animator)

anim.ui.start_app(app, window)

