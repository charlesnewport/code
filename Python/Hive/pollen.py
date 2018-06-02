from vec import *

import pygame

class Pollen:
	def __init__(self, pos=False, disease=None):
		if not pos:
			self.pos = Vector().random2D(400, 400)
		else:
			self.pos = pos
		self.r = 4

		if disease != None and random.random() < 0.5:
			self.disease = disease
		else:
			self.disease = None

	def display(self, screen):
		if self.disease:
			pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.r)
	
		else:
			pygame.draw.circle(screen, (255, 255, 0), (int(self.pos.x), int(self.pos.y)), self.r)
