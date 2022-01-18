import animation
import anim

app = anim.ui.create_app()
scene = anim.scene()
animator = anim.animator()
star_anim = animation.animation(scene, animator)
window = anim.ui.create_app_window(star_anim, scene, animator)

anim.ui.start_app(app, window)

