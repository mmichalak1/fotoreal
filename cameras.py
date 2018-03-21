from rendertypes import *
from colour import Color
import sys
import math
from collisions import *

class ortocam:
	def __init__(self, position, direction, farPlane, width, heigth, stepx, stepy):
		self.position = position
		self.direction = direction
		self.basicOrig = self.position - vector(width / 2, heigth / 2, 0)
		self.stepx = stepx
		self.stepy = stepy
		self.farPlane = farPlane

	
	def parsePixel(self, coord, objects):
		rayOrig = vector(self.basicOrig.x, self.basicOrig.y, self.basicOrig.z)
		rayOrig.x += self.stepx * coord[0]
		rayOrig.y += self.stepy * coord[1]
		# print(rayOrig)
		r = ray(rayOrig, self.direction)
		minDistance = self.farPlane
		hit = None
		# print(objects)
		for obj in objects:
			tmp = r.isColliding(obj)
			if tmp != None:
				distance = (tmp.hitPoint - r.origin).getLength()
				if ( distance < minDistance):
					hit = tmp
					minDistance = distance
		if (hit == None):
			return Color("white")
		else:
			return hit.material
	
class perspectiveCam:
	def __init__(self, position, direction, farPlane, nearPlane, fov, ratio, stepx, stepy):
		self.position = position
		self.direction = direction
		self.nearPlane = nearPlane
		self.farPlane = farPlane
		self.fov = fov
		self.basicOrig = self.position - vector(self.getProjectionWidth / 2, self.getProjectionHeight / 2, -nearPlane)
		self.ratio = ratio
		self.stepx = stepx
		self.stepy = stepy
	def getProjectionWidth(self):
		width = 1/(tan(self.fov/2)) * nearPlane
		return 2*width
	def getProjectionHeight(self):
		heihgt = (1/self.ratio) * self.getProjectionWidth()
		return heigth
	def parsePixel(self, coord, objects):
		rayOrig = vector(self.basicOrig.x, self.basicOrig.y, self.basicOrig.z)
		rayOrig.x += self.stepx * coord[0]
		rayOrig.y += self.stepy * coord[1] 
		
	