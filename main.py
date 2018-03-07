import math


class vector:
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c
	def getLengthPow2(self):
		result = 0
		result += self.a**2 
		result += self.b**2
		result += self.c**2
		return result
	def getLength(self):
		return math.sqrt(self.getLengthPow2())
	def nvector(self):
		return vector(-self.a, -self.b, -self.c)
	def __mul__(self, other):
		if isinstance(other, vector):
			NotImplementedError
		elif isinstance(other, (int, float)):
			return vector(self.a * other, self.b * other, self.c * other)
		else:
			NotImplementedError
	def __str__(self):
		return ("(%d,%d,%d)" % (self.a, self.b, self.c))
	__rmul__ = __mul__
		
		
vec = vector(1, 1, 0)

print(vec.getLength())
print(vec.getLengthPow2())
print(vec.nvector())
print(vec * 2)
print(2 * vec)
