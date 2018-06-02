import pygame

def textBox(screen, text, colour):
	akx, aky = 10, 10
	textSize = 30
	buf = 2

	myfont = pygame.font.SysFont('freesansbold.ttf', textSize, bold=False)

	w = 0
	h = 0
	prev_h = 0

	for t in text:
		tr = myfont.render(t, True, colour)
		tw, th = myfont.size(t)
		if tw > w:
			w = tw
		h += th
		screen.blit(tr, (akx + buf, aky + prev_h + buf))
		prev_h += th

	pygame.draw.rect(screen, colour, (aky, aky, w + buf*2, h + buf), 1)
