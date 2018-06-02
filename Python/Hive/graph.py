import pygame

width = 400
height = 400

class Graph:
	def __init__(self, dataTypes, left=False):
		self.w = 50
		self.h = 50

		self.left = left
		if left:
			self.x = 10
		else:
			self.x = width - 60
		self.y = round((width - (len(dataTypes) * 50)) / (len(dataTypes) + 1), 0)

		self.ys = [[] for i in range(len(dataTypes))]
		self.dataTypes = dataTypes
		self.show = True

	def update(self, data):
		for i in range(len(self.ys)):
			if len(self.ys[i]) > self.w - 1:
				for j in range(len(self.ys[i]) - self.w - 1, -1, -1):
					del(self.ys[i][j])
			if data != None:
				self.ys[i].append(data[self.dataTypes[i]])

	def text(self, message, screen, y):
		textSize = 25
		buf = 2
		colour = (255, 255, 255)
		myfont = pygame.font.SysFont('freesansbold.ttf', textSize, bold=False)

		tr = myfont.render(message, True, colour)
		tw, th = myfont.size(message)
		
		if self.left:
			anchor = (self.x + self.w + 5, y + 2*th/3)
		else:
			anchor = (self.x - tw - 5, y + 2*th/3)
		screen.blit(tr, anchor)

	def display(self, screen):
		if self.show:
			y = self.y
			for i in range(len(self.ys)):
				mouse = pygame.mouse.get_pos()
				if mouse[0] >= self.x and mouse[0] <= self.x + self.w:
					if mouse[1] >= y and mouse[1] <= y + self.h:
						self.text(self.dataTypes[i], screen, y)

				pygame.draw.rect(screen, (0, 0, 0), (self.x, y, self.w, self.h))
				pygame.draw.rect(screen, (255, 255, 255), (self.x, y, self.w, self.h), 1)

				for j in range(1, len(self.ys[i])):
					pygame.draw.line(screen, (255, 255, 255), (self.x + j - 1, y + self.h - self.ys[i][j-1]), (self.x + j, y + self.h - self.ys[i][j]), 1)
				
				y += 50
				y += self.y
