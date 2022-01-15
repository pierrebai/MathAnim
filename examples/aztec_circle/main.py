import animation
import anim

app = anim.ui.create_app()
scene = anim.scene()
animator = anim.animator()
aztec_anim = animation.animation(scene)
window = anim.ui.create_app_window(aztec_anim, scene, animator)

anim.ui.start_app(app, window)

