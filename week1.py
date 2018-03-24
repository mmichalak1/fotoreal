import rendertypes as rt
import collisions as cl
from colour import Color


s = rt.sphere(rt.vector(0,0,10), 2, Color("Red"))
r = rt.ray(rt.vector(), rt.vector(0,0,1))

print(r.isColliding(s))