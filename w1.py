from collisions import *
from rendertypes import *


sph = sphere(vector(), 10)
r1 = ray(vector(0,0,-10), vector(0,0,1))
r2 = ray(vector(0,0,-10), vector(0,1,0))

print("Punkt przecięcia z r1: {}".format(raySphereColl(r1, sph)))
print("Punkt przecięcia z r2: {}".format(raySphereColl(r2, sph)))

r3 = ray(vector(10,-1,0), vector(0, 1, 0))

print("Punkt przecięcia z r3: {}".format(raySphereColl(r3, sph)))

p = plane(vector(), vector(0, 0.5, 0.5).normalize())

print("Punkt przecięcia p1 z r2: {}".format(rayPlaneColl(r2, p)))