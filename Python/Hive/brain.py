from vec import *
import random

def createGene(lower, upper, amount):
	r = [random.randint(lower, upper) for i in range(amount)]
	if len(r) == 1:
		return r[0]
	return r

class Genes:
	def __init__(self):
		self.g1 = [-2, 2, 1] # mult good
		self.g2 = [-2, 2, 1] # mult bad
		self.g3 = [0, 100, 1] # look dist good
		self.g4 = [0, 100, 1] # look dist bad
		self.g5 = [1, 6, 1] # hLimit

	def createGenes(self):
		genes = [self.g1, self.g2, self.g3, self.g4, self.g5]
		rGenes = []
		for g in genes:
			rGenes.append(createGene(g[0], g[1], g[2]))
		return rGenes

class Brain:
	def __init__(self,dna=False):
		if not dna:
			self.dna = []
			g = Genes()
			self.dna = g.createGenes()
		else:
			self.dna = dna

		self.mr = 0.01		

	def calcFitness(self):
		if self.total_eaten > 0:

			self.fitness = (self.food_eaten / self.total_eaten) * self.timeAlive
		else:
			self.fitness = 1

	def createG1(self):
		return random.random() * 4 - 2

	def createG2(self):
		return random.randint(0, 100)

	def createG3(self):
		return random.randint(1, 6)

	def crossover(self, partner):
		newDNA = []
		for i in range(len(self.dna)):
			if random.random() < 0.5:
				newDNA.append(self.dna[i])
			else:
				newDNA.append(partner.dna[i])
		return Brain(newDNA)

	def mutate(self):
		if random.random() < self.mr:
			self.dna[0] = self.createG1()
		if random.random() < self.mr:
			self.dna[1] = self.createG1()
		if random.random() < self.mr:
			self.dna[2] = self.createG2()
		if random.random() < self.mr:
			self.dna[3] = self.createG2()
		if random.random() < self.mr:
			self.dna[4] = self.createG3()
