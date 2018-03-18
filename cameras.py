from rendertypes import *
from colour import Color
import sys
from collisions import *

class ortocam:
	def __init__(self, position, direction, width, heigth, stepx, stepy):
		self.position = position
		self.direction = direction
		self.basicOrig = self.position - vector(width / 2, heigth / 2, 0)
		self.stepx = stepx
		self.stepy = stepy
	
	def parsePixel(self, coord, objects):
		rayOrig = vector(self.basicOrig.x, self.basicOrig.y, self.basicOrig.z)
		rayOrig.x += self.stepx * coord[0]
		rayOrig.y += self.stepy * coord[1]
		# print(rayOrig)
		r = ray(rayOrig, self.direction)
		minDistance = sys.float_info.max
		hit = None
		# print(objects)
		for obj in objects:
			tmp = raySphereColl(r, obj)
			if tmp != None:
				distance = (tmp.hitPoint - r.origin).getLength()
				if ( distance < minDistance):
					hit = tmp
					minDistance = distance
		if (hit == None):
			return Color("white")
		else:
			return hit.material
	
		
	