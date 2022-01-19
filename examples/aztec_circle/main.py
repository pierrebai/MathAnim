import animation
import anim

app = anim.ui.create_app()
scene = anim.scene()
animator = anim.animator()
the_anim = animation.animation(scene, animator)
window = anim.ui.create_app_window(the_anim, scene, animator)

anim.ui.start_app(app, window)

