import pygame

width = 400
height = 400

class Options:
	def __init__(self):
		self.x = 80
		self.w = width - self.x * 2
		self.h = 50
		self.y = height - self.h - 10

		self.selected = False
		self.show = False

	def update(self, mouse):
		if self.show:
			if mouse[0] >= self.x and mouse[0] <= self.x + self.w and mouse[1] >= self.y and mouse[1] <= self.y + self.h:
				self.selected = not self.selected

	def display(self, screen):
		if self.show:
			if self.selected:
				pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.w, self.h))
			else:
				pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 1)
			pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 1)
