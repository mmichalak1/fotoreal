from collisions import *
from rendertypes import *
from colour import Color


pl = plane(vector(0,0,1), vector(0,0,1), Color("Blue"))

r = ray(vector(), vector(0,0,1))

print(r.isColliding(pl))