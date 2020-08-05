import pygame
from board_class import Board, Minotaur, Player
pygame.init()

# Set up board_class objects
maze = Board(maze_key={'size_board': (5, 5), 'walls': [((0, 4), (1, 4)), ((1, 1), (2, 1)), ((1, 1), (1, 2)), ((1, 2), (2, 2)), ((1, 3), (2, 3)), ((2, 0), (2, 1)), ((2, 2), (3, 2)), ((2, 2), (2, 3)), ((3, 0), (4, 0)), ((3, 1), (4, 1)), ((3, 2), (4, 2)), ((4, 3), (4, 4))], 'player_start': (2, 2), 'mino_start': (4, 0), 'goal': (4, 0), 'solution': ['up', 'right', 'up', 'left', 'left', 'left', 'down', 'down', 'down', 'up', 'up', 'right', 'up', 'right', 'right', 'left', 'left', 'left', 'down', 'down', 'right', 'down', 'down', 'right', 'right', 'up', 'right', 'up', 'up', 'up'], 'sol_length': 30, 'seed': 7007840853224901478})

class PlayerToken:
	def __init__(self, start, board):
		self.x = start[0]
		self.y = start[1]
		self.v = 50

		self.player = Player(board)

class MinoToken:
	def __init__(self, start, board):
		self.x = start[0]
		self.y = start[1]

		self.mino = Minotaur(board)

player_token = PlayerToken(start = (50,50), board = maze)
mino_token = MinoToken(start = (100,100), board = maze)

def calculate_screen_size(board):
	# Take in board, specifically size_board. 
	# Return the dimensions of the screen that will accommodate that board size. 
	# The maximum window size that the display on my MacBook can comfortably acommodate is (1400, 800)
	# So if I set each tile to be 100px, then I should start scaling for boards larger than 7x7. 

	size_board = board.G.graph["size_board"]

	# Set edge buffer to be 50 px
	screen_buffer = 50







# Set window size
window = pygame.display.set_mode(size = (1400,800))
# window.fill((255,255,255)) # Fills the screen with white
# pygame.display.update()
pygame.display.set_caption("Minotaur Project")

run = True
while run:
	# pygame.time.delay(10) # Wait 10 ms between cycles. 

	# Get keyboard press events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			# Get KEYDOWN so that holding a key will not trigger repeated movements.
			if event.key == pygame.K_w or event.key == pygame.K_UP:
				# Up
				player_token.y -= player_token.v
			if event.key == pygame.K_a or event.key == pygame.K_LEFT:
				# Move left
				player_token.x -= player_token.v
			if event.key == pygame.K_s or event.key == pygame.K_DOWN:
				# Down
				player_token.y += player_token.v
			if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
				# Right
				player_token.x += player_token.v
	
	# Redraw Window
	window.fill((255,255,255)) # Fills the screen with black
	pygame.draw.line(surface = window, color = (0,0,0), start_pos = (50,50), end_pos = (50, 200), width = 10)
	pygame.draw.circle(surface = window, color = (0,0,255), center = (player_token.x, player_token.y), radius = 15)
	pygame.draw.circle(surface = window, color = (255,0,0), center = (mino_token.x, mino_token.y), radius = 40)
	pygame.display.update()
	
pygame.quit()