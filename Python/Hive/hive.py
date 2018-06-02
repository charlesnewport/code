from pollen import *
from brain import *
from text import *
from vec import *
from bee import *

import random
import pygame
import math
import copy

width = 400
height = 400

def area(r):
	return math.pi * (r ** 2)

def radius(a):
	return math.sqrt(a / math.pi)

class Hive:
	def __init__(self, x=False, y=False):
		#location
		if not x and not y:
			self.x = random.randint(0, width)
			self.y = random.randint(0, height)
		else:
			self.x = x
			self.y = y
		self.pos = Vector(self.x, self.y)

		#display
		self.colour = [random.randint(0, 255) for i in range(3)]
		self.chosen = False
		self.carn = False

		#values for bee
		self.hiveMind = Brain()
		self.disease = None

		self.bees = [Bee(self.x, self.y, self.colour, Vector(self.x, self.y), self.hiveMind, self.disease) for i in range(3)]

		#popping
		self.popCount = 0
		self.pop = 15
		self.r = 3

	def et(self):
		for b in self.bees:
			b.et()

	def inBounds(self, v):
		if v.x <= width and v.x >= 0 and v.y <= height and v.y >= 0:
			return True
		return False

	def update(self, pollen, poison, mondo):
		for i in range(len(self.bees)-1, -1, -1):
			#update/eat
			self.bees[i].boundaries()
			self.bees[i].behaviours(pollen, poison)
			self.bees[i].update(self)

			#dead?
			nB = self.bees[i].clone()
			if nB != None:
				self.bees.append(nB)
			if self.bees[i].dead():
				#adding food
				if self.inBounds(self.bees[i].pos):
					if self.bees[i].disease == None: 
						mondo.pollen.append(Pollen(self.bees[i].pos, self.bees[i].disease))
					else:
						mondo.poison.append(Pollen(self.bees[i].pos, self.bees[i].disease))
				del(self.bees[i])

		#pop?
		self.reprod()

	def queen(self):
		nQs = []
		for i in range(len(self.bees)-1, -1, -1):
			if self.bees[i].queen() and self.inBounds(self.bees[i].pos):
				nQs.append(Hive(int(self.bees[i].pos.x), int(self.bees[i].pos.y)))
				del(self.bees[i])
		return nQs

	def dead(self):
		return len(self.bees) == 0

	#display info
	def age(self):
		yg = 0
		og = 1000000
		for b in self.bees:
			if b.generation > yg:
				yg = b.generation
			if b.generation < og:
				og = b.generation
		return yg, og

	def dInfo(self):
		if self.disease == None:
			return self.disease
		else:
			return self.disease.name

	def chosenData(self):
		data = {}
		data['Bees'] = len(self.bees)
		data['Infected'] = self.countInfected()
		data['Percent Infected'] = self.countInfected() / len(self.bees) * 50
		data['Pops'] = self.popCount
		data['Average age'] = sum([b.generation for b in self.bees])/len(self.bees)
		data['Average health'] = sum([b.health for b in self.bees])/len(self.bees) * 50
		return data

	def countInfected(self):
		return sum([1 for b in self.bees if b.disease != None])
	##

	def display(self, screen, legend=False):
		for b in self.bees:
			b.display(screen, legend)
		pygame.draw.circle(screen, self.colour, (self.x, self.y), int(self.r))

		if self.disease != None:
			pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), int(self.r + 1), 1)

		if self.chosen:
			pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), int(self.r + 1), 1)

			for b in self.bees:
				pygame.draw.line(screen, self.colour, (self.x, self.y), (int(b.pos.x), int(b.pos.y)), 1)

	def reprod(self):
		if self.r >= self.pop:
			self.r = 5
			self.popCount += 1
			self.bees += [Bee(self.x, self.y, self.colour, Vector(self.x, self.y), self.hiveMind, self.disease) for i in range(3)]

	def grow(self, rs):
		a = [area(r.r) for r in rs]
		a.append(area(self.r))
		cA = sum(a)
		self.r = radius(cA)
