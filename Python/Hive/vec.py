import numpy as np
import random
import math

def dist(x1, y1, x2, y2):
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def map(x, x1, y1, x2, y2):
	return (x - x1) / (y1 - x1) * (y2 - x2) + y2

class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		self.z = 0

	def log(self):
		print(self.x, self.y, self.z)

	def random2D(self, x=False, y=False):
		if not x and not y:
			self.x = np.random.random() * 2 - 1
			self.y = np.random.random() * 2 - 1
		else:
			self.x = random.randint(0, x)
			self.y = random.randint(0, y)
		return Vector(self.x, self.y)

	def normalize(self):
		l = self.mag()
		if l != 0:
			self.mult(1/l)
		return self

	def dist(self, v):
		return math.sqrt((self.x - v.x)**2 + (self.y - v.y)**2)

	def setMag(self, n):
		return self.normalize().mult(n)

	def magSq(self):
		x = self.x
		y = self.y
		z = self.z
		return x*x + y*y + z*z

	def mag(self):
		return math.sqrt(self.magSq())	

	def sub(self, v):
		self.x -= v.x
		self.y -= v.y

	def add(self, v):
		self.x += v.x
		self.y += v.y

	def mult(self, n):
		self.x *= n
		self.y *= n
		self.z *= n

	def div(self, n):
		self.x /= n
		self.y /= n
		self.z /= n

	def limit(self, m):
		magSq = self.magSq()
		if magSq > m ** 2:
			self.div(math.sqrt(magSq))
			self.mult(m)
