import math

class ray:
	def __init__(self,origin,direction, distance = 0):
		self.origin = origin
		self.direction = direction
		self.distance = distance
	def __setattr__(self, name, value):
		if name in ['origin','direction'] and not isinstance(value, vector):
			raise TypeError('ray.{} must be of type: vector'.format(name))
		if name == 'distance' and not isinstance(value, (int, float)):
			raise TypeError('ray.distance must be a number')
		super().__setattr__(name, value)
	def __str__(self):
		if (self.distance <= 0):
			return ("(origin:{}, direction:{})".format(self.origin, self.direction))
		else:
			return ("(origin:{}, direction:{}, distance:{})".format(self.origin, self.direction, self.distance))

class sphere:
	def __init__(self,center,radius):
		self.center = center
		self.radius = radius
	# walić pythona ja chce moje typy zmiennych
	def __setattr__(self, name, value):
		if name == 'center' and not isinstance(value, vector):
			raise TypeError('sphere.center must be of type: vector')
		super().__setattr__(name, value)
	def __str__(self):
		return ("(center:{}, radius:{})".format(self.center, self.radius))

class plane:
	def __init__(self,point,normal):
		self.point = point
		self.normal = normal
	def __setattr__(self, name, value):
		if name in ['point','normal'] and not isinstance(value, vector):
			raise TypeError('sphere.{} must be of type: vector'.format(name))
		super().__setattr__(name, value)
	def __str__(self):
		return ("(point on plane:{}, normal:{})".format(self.point, self.normal))
	
#self note: dot jest pod mnozeniem/scalar a cross pod funkcja cross
class vector:
	def __init__(self, a=0, b=0, c=0):
		self.x = a
		self.y = b
		self.z = c
	def getLengthPow2(self):
		result = 0
		result += self.x**2 
		result += self.y**2
		result += self.z**2
		return result
	def getLength(self):
		return math.sqrt(self.getLengthPow2())
	def nvector(self):
		return vector(-self.x, -self.y, -self.z)
	def __mul__(self, other):
		if isinstance(other, vector):
			return self.x * other.x + self.y * other.y + self.z * other.z
		elif isinstance(other, (int, float)):
			return vector(self.x * other, self.y * other, self.z * other)
		else:
			NotImplementedError
	def __floordiv__(self, other):
		if isinstance(other, vector):
			return vector(self.x//other.x, self.y//other.y, self.z//other.z)
		elif isinstance(other, (int, float)):
			if (other == 0):
				ZeroDivisionError
			else:
				return vector(self.x//other, self.y//other, self.z//other)

		else:
			NotImplementedError
	def __truediv__(self, other):
		if isinstance(other, vector):
			return vector(self.x/other.x, self.y/other.y, self.z/other.z)
		elif isinstance(other, (int, float)):
			if (other == 0):
				ZeroDivisionError
			else:
				return vector(self.x/other, self.y/other, self.z/other)
		else:
			NotImplementedError
	def __add__(self, other):
		return vector(self.x + other.x, self.y + other.y, self.z + other.z)
	def __sub__(self, other):
		return vector(self.x - other.x, self.y - other.y, self.z - other.z)
	def __eq__(self, other):
		if not isinstance(other, vector):
			NotImplementedError
		return self.x == other.x and self.y == other.y and self.z == other.z
#te już znowu potrzebne
	def scalar(self, vect):
		return ((self.x * vect.x) + (self.y * vect.y) + (self.z * vect.z))
	def cross(self, vect):
		return vector(self.y*vect.z - self.z*vect.y, self.z*vect.x - self.x*vect.z,self.x*vect.y - self.y * vect.x)
	def normalize(self):
		if (self.getLength() != 0):
			vect = vector(self.x,self.y,self.z)
			vect.x /= self.getLength()
			vect.y /= self.getLength()
			vect.z /= self.getLength()
			return vect
	def __str__(self):
		return ("({},{},{})".format(self.x, self.y, self.z))
	def __neg__(self):
		return vector(-self.x, -self.y, -self.z)
	__rmul__ = __mul__
	__radd__ = __add__	
