from disease import *
from options import *
from pollen import *
from graph import *
from hive import *

import pygame
import random
import sys

width = 400
height = 400

class ilMondo:
	def __init__(self):
		self.hives = [Hive() for i in range(4)]
		self.pollen = [Pollen() for i in range(10)]
		self.poison = []

		self.legend = False
		self.pause = False

		self.overload = 50

		self.graph1 = Graph(['Bees', 'Infected', 'Percent Infected', 'Pops', 'Average age', 'Average health'])
		self.graph2 = Graph(['Hives', 'Pollen', 'Population', 'Diseased'], True)
		self.options = Options()

	def chosenReset(self):
		for h in self.hives:
			h.chosen = False

	def chosenData(self):
		for h in self.hives:
			if h.chosen:
				return h.chosenData()
		return None

	def info(self):
		data = {}
		data['Hives'] = len(self.hives)
		data['Pollen'] = len(self.pollen)
		data['Population'] = sum([len(h.bees) for h in self.hives])
		data['Diseased'] = sum([h.countInfected() for h in self.hives])
		return data

	def food(self):
		return [p for p in self.pollen if p.disease == None], [p for p in self.pollen if p.disease != None]

	def test(self, i):
		food = []
		for j in range(len(self.hives)):
			if j != i:
				food += self.hives[j].bees
		return food

	def events(self, screen):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_l:
					self.legend = not self.legend
				elif event.key == pygame.K_SPACE:
					self.pause = not self.pause
				elif event.key == pygame.K_g:
					self.graph1.show = not self.graph1.show
				elif event.key == pygame.K_t:
					self.graph2.show = not self.graph2.show
				elif event.key == pygame.K_h:
					for h in self.hives:
						if h.chosen:
							h.et()
							break
				elif event.key == pygame.K_o:
					self.options.show = not self.options.show
				elif event.key == pygame.K_ESCAPE:
					self.chosenReset()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse = event.pos
				m_vector = Vector(mouse[0], mouse[1])
				for i in range(len(self.hives)):
					if self.hives[i].pos.dist(m_vector) < self.hives[i].r:
						self.chosenReset()
						self.hives[i].chosen = True
						break
				self.options.update(mouse)
						
			elif event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		mouse = pygame.mouse.get_pos()
		for h in self.hives:
			m = Vector(mouse[0], mouse[1])
			if m.dist(h.pos) < h.r * 2:
				textBox(screen, 
					    ['Bees: {}'.format(len(h.bees)), 
						 'Radius: {}'.format(int(h.r)), 
						 'Oldest generation: {}'.format(h.age()[1]), 
						 'Youngest generation: {}'.format(h.age()[0]),
						 'Disease: {}'.format(h.dInfo())], 
						  h.colour)

				for b in h.bees:
					pygame.draw.line(screen, h.colour, (h.x, h.y), (int(b.pos.x), int(b.pos.y)), 1)

			for b in h.bees:
				if m.dist(b.pos) < b.r * 2:
					pygame.draw.line(screen, h.colour, (h.x, h.y), (int(b.pos.x), int(b.pos.y)), 1)
					b.drawDists(screen)						
					textBox(screen, b.info(), h.colour)


	def update(self):
		if not self.pause:
			if random.random() < 0.05:
				self.pollen.append(Pollen())

			for i in range(len(self.hives)-1, -1, -1):
				if self.hives[i].carn:
					self.hives[i].update(self.test(i), self.poison, self)
				else:
					self.hives[i].update(self.pollen, self.poison, self)

				if self.hives[i].dead():
					del(self.hives[i])

			for h in self.hives:
				self.hives += h.queen()

			for h in self.hives:
				if h.chosen:
					h.carn = self.options.selected

			self.graph1.update(self.chosenData())			
			self.graph2.update(self.info())

	def display(self, screen):
		for h in self.hives:
			h.display(screen, self.legend)

		for p in self.pollen:
			p.display(screen)

		for p in self.poison:
			p.display(screen)

		self.graph1.display(screen)
		self.graph2.display(screen)
		self.options.display(screen)

		pygame.display.set_caption('Number of hives: {} Total population: {}'.format(len(self.hives), sum([len(h.bees) for h in self.hives])))
		# pygame.display.set_caption('FPS: {}'.format(clock.get_fps()))

	def run(self):
		pygame.init()
		pygame.font.init()
		screen = pygame.display.set_mode((width, height))
		clock = pygame.time.Clock()

		while len(self.hives) > 0:
			screen.fill((0, 0, 0))
			
			self.update()
			self.events(screen)
			self.display(screen)

			if len(self.hives) <= self.overload:
				pygame.display.update()
				clock.tick(30)

m = ilMondo()
m.run()