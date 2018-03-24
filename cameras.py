from rendertypes import *
from colour import Color
import sys
import math
from collisions import *

class ortocam:
	def __init__(self, position, direction, upVector, farPlane, width, heigth, stepx, stepy):
		self.position = position
		self.direction = direction
		self.upVector = upVector
		self.rightVector = upVector.cross(direction)
		self.basicOrig = self.position
		self.basicOrig -= self.rightVector * (width / 2) * stepx
		self.basicOrig -= self.upVector * (heigth / 2) * stepy
		self.stepx = stepx
		self.stepy = stepy
		self.farPlane = farPlane
		# print(self.rightVector)
	
	def parsePixel(self, coord, objects):

		rayOrig = vector(self.basicOrig)
		rayOrig += self.rightVector * self.stepx * coord[0]
		rayOrig += self.upVector * self.stepy * coord[1]
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
	def __init__(self, position, direction, upVector, farPlane, nearPlane, fov, width, height, stepx, stepy):
		self.position = position
		self.direction = direction
		self.upVector = upVector
		self.nearPlane = nearPlane
		self.farPlane = farPlane
		self.fov = fov
		self.width = width
		self.height = height
		self.stepx = stepx
		self.stepy = stepy
		self.basicOrig = (position+(direction.normalize()*self.getProjectionDistance())) - ((upVector.normalize().cross(direction.normalize()))*(width / 2)) - (upVector.normalize() * (height/ 2))
		print(self.basicOrig)
		print((upVector.normalize().cross(direction.normalize())))
	def getProjectionDistance(self):
		distance = (math.tan(math.radians(self.fov/2))) * self.width/2
		return distance
	def parsePixel(self, coord, objects):
		rayOrig = vector(self.basicOrig.x, self.basicOrig.y, self.basicOrig.z)
		rayOrig += self.upVector.normalize().cross(self.direction.normalize()) * (self.stepx * coord[0])
		rayOrig += self.upVector.normalize() * self.stepy * coord[1]
		r = ray(self.position, (rayOrig - self.position).normalize())
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