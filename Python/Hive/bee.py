from disease import *
from pollen import *
from brain import * 
from vec import *

import pygame
import random
import math

mr = 0.01

width = 400
height = 400

class Bee:
	def __init__(self, x, y, colour, home, brain=False, disease=None, generation=0):
		#dna
		if not brain:
			self.brain = Brain()
		else:
			self.brain = brain
			self.brain.mutate()
		self.dna = self.brain.dna

		self.multG = self.dna[0]
		self.multB = self.dna[1]

		self.distG = self.dna[2]
		self.distB = self.dna[3]

		self.hLimit = self.dna[4]

		# self.hDecline = self.dna[5]
		# self.maxForce = self.dna[6]
		# self.maxSpeed = self.dna[7]
		# self.reprodRate = self.dna[8]
		# self.queenRate = self.dna[9]
		# self.hiveLoc = self.dna[10]

		#generation
		self.generation = generation

		#movement
		self.vel = Vector(0, -2)
		self.acc = Vector().random2D()
		self.pos = Vector(x, y)

		#make these part of dna?
		self.maxForce = 0.5
		self.maxSpeed = 5

		#display
		self.colour = colour
		self.r = 4

		#food/targeting
		self.holding = []
		self.goHome = False
		self.home = home

		#health
		self.health = 1
		self.disease = disease
		self.kill = False

	def dInfo(self):
		if self.disease == None:
			return self.disease
		else:
			return self.disease.name

	def queen(self):
		return random.random() < 0.0003
		# return random.random() < self.queenRate

	def update(self, hive):
		if random.random() < 0.0003:
			self.disease = Disease()

		if self.disease != None:
			self.disease.effects(self)

		if len(self.holding) >= self.hLimit or self.goHome:
			steerH = self.seek(self.home)
			steerH.mult(self.dna[0])
			self.applyForce(steerH)

		if self.pos.dist(self.home) < self.r + hive.r:
			hive.grow(self.holding)
			self.holding = []

			if self.disease == None:
				self.disease = hive.disease
			else:
				hive.disease = self.disease

			self.goHome = False

		self.health -= 0.005
		self.vel.add(self.acc)
		self.vel.limit(self.maxSpeed)
		self.pos.add(self.vel)
		self.acc.mult(0)

	def applyForce(self, force):
		self.acc.add(force)

	def behaviours(self, good, bad):
		steerG = self.eat(good, self.distG)
		steerG.mult(self.multG)
		self.applyForce(steerG)
	
		steerB = self.eat(bad, self.distB)
		steerB.mult(self.multB)
		self.applyForce(steerB)

	def clone(self):
		if random.random() < 0.003:
		# if random.random() < self.reprodRate:
			return Bee(self.pos.x, self.pos.y, self.colour, self.home, self.brain, self.disease, self.generation + 1)
		else:
			return None

	def et(self):
		self.goHome = True

	def eat(self, list, perception):
		record = math.inf
		closest = None
		for i in range(len(list)-1, -1, -1):
			d = self.pos.dist(list[i].pos)
			if d < self.r + list[i].r:
				self.holding.append(list[i])
				if self.disease == None:
					self.disease = list[i].disease

				self.health += 0.2
				if isinstance(list[i], Bee):
					list[i].kill = True
				else:
					del(list[i])

			else:
				if d < record and d < perception:
					#could go for largest?
					record = d
					closest = list[i]
		if closest != None:
			return self.seek(closest.pos)
		return Vector(0, 0)

	def seek(self, target):
		desired = Vector(target.x, target.y)
		desired.sub(self.pos)
		desired.setMag(self.maxSpeed)
		steer = Vector(desired.x, desired.y)
		steer.sub(self.vel)
		steer.limit(self.maxForce)
		return steer

	def dead(self):
		return self.health < 0 or self.kill

	def drawDists(self, screen):
		try:
			pygame.draw.circle(screen, (0, 255, 0), (int(self.pos.x), int(self.pos.y)), self.distG, 1)
		except:
			None
		try:
			pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.distB, 1)
		except:
			None

	def display(self, screen, legend=False):
		if legend:
			self.drawDists(screen)
		pygame.draw.circle(screen, self.colour, (int(self.pos.x), int(self.pos.y)), self.r)

		if self.disease != None:
			pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), int(self.r + 1), 1)

	def info(self):
		return ['Health: {}'.format(round(self.health, 2)),
				'Holding: {}'.format(len(self.holding)),
				'hLimit: {}'.format(self.hLimit),
				'Generation: {}'.format(self.generation),
				'MultG: {}'.format(round(self.multG, 2)),
				'MultB: {}'.format(round(self.multB, 2)),
				'Disease: {}'.format(self.dInfo())]

	def boundaries(self):
		d = 25
		desired = None

		if self.pos.x < d:
			desired = Vector(self.maxSpeed, self.vel.y)
		elif self.pos.x > width - d:
			desired = Vector(-self.maxSpeed, self.vel.y)

		if self.pos.y < d:
			desired = Vector(self.vel.x, self.maxSpeed)
		elif self.pos.y > height - d:
			desired = Vector(self.vel.x, -self.maxSpeed)

		if desired != None:
			desired.normalize()
			desired.mult(self.maxSpeed)
			steer = Vector(desired.x, desired.y)
			steer.sub(self.vel)
			steer.limit(self.maxForce)
			self.applyForce(steer)