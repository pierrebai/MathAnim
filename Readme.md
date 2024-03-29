# Maths Animation

This is a Python module to create animations of maths demonstrations
as seen in the Mathologer YouTube channel.

The module defines an animation as a serie of shots containing actors
and the movements of these actors. The playback is managed by an
animator.

The actors are points, lines, circles, polygons, or any other objects.
The geometric objects are defined by points and it is these points that
are animated, moving the objects that uses them. This simplifies the
animation of linked objects. For example a line drawn between two
circle centers will move when the circles move.

Furthermore, points themselves can be defined relative to another
point. That other point is called their origin. Such relative point
move when their origin moves. This allows to create a hierarchy of
points and complex animations.

The module provide ready-made simple animation formulas, for example
to move a point or rotate it around another point.

In addition to the geometry, the module manages what gets drawn. Each
actor is given a name. The decision to draw or not each actor is
decided by an option linked to its name. All actors with the same
name are controlled by the same option.

The overall demonstration can also define parameters that will
automatically generate user-controllable options to modify them.
For example, a demonstration involving a polygon could let the user
choose the number of sides of the polygon.

## Examples

The modules comes with many examples. Currently, there are Seven, but
more will be added later. The examples are:

### Aztec Circle
Based on this [Mathologer video](https://www.youtube.com/watch?v=Yy7Q8IWNfHM)

![Aztec Circle](https://github.com/pierrebai/MathAnim/blob/main/examples/aztec_circle/Aztec-Circle.png "Aztec Circle")

### Rotating Stars

Based on this [Mathologer video](https://www.youtube.com/watch?v=oEN0o9ZGmOM&t=1261s)

![Rotating Stars](https://github.com/pierrebai/MathAnim/blob/main/examples/rotating_stars/Rotating-Stars.png "Rotating Stars")

### Geometric Sum of Quarters

Based on this [Mathologer video](https://www.youtube.com/watch?v=SOBz-aFOH2I)

![Quarter Sum](https://github.com/pierrebai/MathAnim/blob/main/examples/quarter_geometric_sum/Quarter-Sum.png "Quarter Sum")

### Vortex Maths

Based on this [Mathologer video](https://www.youtube.com/watch?v=6ZrO90AI0c8&t=7s)

![Vortex Maths](https://github.com/pierrebai/MathAnim/blob/main/examples/vortex_maths/Vortext-Maths.png "Vortex Maths")

### Three Bisectors

Base on this [Mathologer video](https://www.youtube.com/watch?v=XOS73mTomPY)

![Three Bisectors](https://github.com/pierrebai/MathAnim/blob/main/examples/three_bisectors/Three-Bisectors.png "Three Bisectors")

### Pentagramaths

Base on this [Mathologer video](https://www.youtube.com/watch?v=w4AUOgfW9NI)

![Pentagramaths](https://github.com/pierrebai/MathAnim/blob/main/examples/pentagramaths/Pentagramaths.png "Pentagramaths")

### Lonely Runner

Base on this [Wikipedia page](https://en.wikipedia.org/wiki/Lonely_runner_conjecture)

![Lonely Runner](https://github.com/pierrebai/MathAnim/blob/main/examples/lonely_runner/Lonely_Runner.png "Lonely Runner")
