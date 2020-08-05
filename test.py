import pygame
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Test")

run = True

while run:
	pygame.time.delay(1000)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				





	
	pygame.display.update() 
	
pygame.quit()