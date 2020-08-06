import pygame
from board_class import Board, Minotaur, Player
from file_io import get_maze
pygame.init()

maze_key = get_maze(size = "large", difficulty = "max")
print("Maze key retrieved.")
print(maze_key)

# Set up board_class objects
maze = Board(maze_key)

player = Player(maze)
mino = Minotaur(maze)
# Add extra moves to make animation work easily
player_moves = [maze.G.graph["player_location"], maze.G.graph["player_location"]]
mino_moves = [maze.G.graph["mino_location"], maze.G.graph["mino_location"], maze.G.graph["mino_location"]]


def calculate_screen_size(board):
	# Take in board, specifically size_board. 
	# Return the dimensions of the screen that will accommodate that board size. 
	# The maximum window size that the display on my MacBook can comfortably acommodate is (1400, 800)
	# So if I set each tile to be 100 px, then I should start scaling for boards larger than 7x7. 

	size_board = board.G.graph["size_board"]

	# Define unscaled tile size
	tile_size = 100 # 100 px

	# Set edge buffer to be 50 px
	screen_buffer = 50

	# Set scaling factor
	scale_factor = 0.5

	# Scale the tile and board size if using a board with any dimension greater than 7. 
	max_board_dim = max(size_board[0], size_board[1])
	if max_board_dim > 7:
		scaled = True
		tile_size_scaled = int(tile_size * scale_factor)
	else:
		scaled = False
		tile_size_scaled = tile_size

	size_window = (size_board[0]*tile_size_scaled + screen_buffer*2, size_board[1]*tile_size_scaled + screen_buffer*2)
	
	return size_window, tile_size_scaled, screen_buffer

def draw_board(board, window, player_moves, mino_moves, win_message = " ", display_win_message = False):
	# Get the window size to be drawn
	size_window, tile_size_scaled, screen_buffer = calculate_screen_size(maze)
	screen_buffer = 50

	# Animation constants
	fps = 60
	time_to_move = 0.1
	frames = int(fps*time_to_move)

	def adj_token_coordinates(coordinates):
		# Take in coordinates (x, y) that correspond to G.graph coordinates, and output new coordinates for the window. 
		# New coordinate assumes that token is drawn at center of token.

		# (x, y) -> (screen_buffer + tile_size_scaled*x + tile_size_scaled/2, screen_buffer + tile_size_scaled*y + tile_size_scaled/2)
		adj_coordinates = (screen_buffer + tile_size_scaled*coordinates[0] + tile_size_scaled/2, screen_buffer + tile_size_scaled*coordinates[1] + tile_size_scaled/2)

		return adj_coordinates

	def adj_wall_coordinates(wall):
		# Wall is ((x1, y1), (x2, y2))
		# Need to get window coordinates based on graph coordinates. 

		x1 = wall[0][0]
		y1 = wall[0][1]
		x2 = wall[1][0]
		y2 = wall[1][1]

		if (y2 - y1) == 0:
			# Vertical
			# Set coordinates such that pos 1 is left of pos 2
			if x1 > x2:
				x1, x2 = x2, x1
				y1, y2 = y2, y1
			# (x1, y1) -> (x1 + 0.5, y1 - 0.5) -> adj_token_coordinates
			# (x2, y2) -> (x2 - 0.5, y2 + 0.5) -> adj_token_coordinates
			return (adj_token_coordinates((x1 + 0.5, y1 - 0.5)), adj_token_coordinates((x2 - 0.5, y2 + 0.5)))
		elif (x2 - x1) == 0:
			# Horizontal
			# Set coordinates such that pos 1 is above of pos 2
			if y1 > y2:
				x1, x2 = x2, x1
				y1, y2 = y2, y1
			# (x1, y1) -> (x1 - 0.5, y1 + 0.5) -> adj_token_coordinates
			# (x2, y2) -> (x2 + 0.5, y2 - 0.5) -> adj_token_coordinates
			return (adj_token_coordinates((x1 - 0.5, y1 + 0.5)), adj_token_coordinates((x2 + 0.5, y2 - 0.5)))
 
	def get_animation_pos(before, after, current_frame, max_frames):
		# Before and after are coordinates
		# current frame is between 1 and max_frames inclusive
		# Return a coordinate between before and after depending on current frame.
		x = before[0] + (current_frame/max_frames)*(after[0]-before[0])
		y = before[1] + (current_frame/max_frames)*(after[1]-before[1])

		return (x, y)

	# Draw walls
	def draw_walls():
		wall_width = int(tile_size_scaled/10)
		width_buffer = wall_width / 2 - 1
		# Draw grids
		# Vertical
		for i in range(1, board.G.graph["size_board"][0]):
			pygame.draw.line(surface = window, color = (230,230,230), start_pos = (screen_buffer + tile_size_scaled*i, screen_buffer - width_buffer), end_pos = (screen_buffer + tile_size_scaled*i, size_window[1] - screen_buffer + width_buffer), width = wall_width)
		# Horizontal
		for i in range(1, board.G.graph["size_board"][1]):
			pygame.draw.line(surface = window, color = (230,230,230), start_pos = (screen_buffer - width_buffer, screen_buffer + tile_size_scaled*i), end_pos = (size_window[0] - screen_buffer + width_buffer, screen_buffer + tile_size_scaled*i), width = wall_width)
		# Draw outer boarder
		# Top
		pygame.draw.line(surface = window, color = (0,0,0), start_pos = (screen_buffer - width_buffer, screen_buffer), end_pos = (size_window[0] - screen_buffer + width_buffer, screen_buffer), width = wall_width)
		# Left
		pygame.draw.line(surface = window, color = (0,0,0), start_pos = (screen_buffer, screen_buffer - width_buffer), end_pos = (screen_buffer, size_window[1] - screen_buffer + width_buffer), width = wall_width)
		# Right
		pygame.draw.line(surface = window, color = (0,0,0), start_pos = (size_window[0] - screen_buffer, screen_buffer - width_buffer), end_pos = (size_window[0] - screen_buffer, size_window[1] - screen_buffer + width_buffer), width = wall_width)
		# Bottom
		pygame.draw.line(surface = window, color = (0,0,0), start_pos = (screen_buffer - width_buffer, size_window[1] - screen_buffer), end_pos = (size_window[0] - screen_buffer + width_buffer, size_window[1] - screen_buffer), width = wall_width)
		# Draw walls
		# Get list of wall coordinate pairs
		walls = []
		for edge, weight in board.G.edges.items():
			if weight["weight"] == -1:
				edge_as_list = []
				for node in edge:
					edge_as_list.append(list(node))
				walls.append(list(edge_as_list))
		for wall in walls:
			w1, w2 = adj_wall_coordinates(wall)
			wx1, wy1 = w1
			wx2, wy2 = w2

			# Width buffers are added differently for horizontal and vertical walls. 
			# Determine if wall segment is vertical or horizontal. 
			if (wx2 - wx1) == 0:
				# Vertical
				pygame.draw.line(surface = window, color = (0,0,0), start_pos = (wx1, wy1 - width_buffer), end_pos = (wx2, wy2 + width_buffer), width = wall_width)
			elif (wy2 - wy1) == 0:
				# Horizontal
				pygame.draw.line(surface = window, color = (0,0,0), start_pos = (wx1 - width_buffer, wy1), end_pos = (wx2 + width_buffer, wy2), width = wall_width)
	
	# Draw text
	def draw_text(display_win_message = False, player_moves = player_moves, mino_moves = mino_moves):
		# The only way to implement the undo option the way I want it to is to amend the move list before the moves are counted.
 
		num_moves = len(player_moves) - 2 # Subtract 2 for the two elements added at initialization
		
		# Draw Font
		# Win message
		if display_win_message:
			font_win_message = pygame.font.Font('freesansbold.ttf', 32) 
			text_win_message = font_win_message.render(win_message, True, (0,0,0)) # (text, antialias, color)
			textRect_win_message = text_win_message.get_rect()  
			textRect_win_message.center = (size_window[0] // 2, 25)
			window.blit(text_win_message, textRect_win_message)

		# Move count
		font_move_count = pygame.font.Font('freesansbold.ttf', 24) 
		text_move_count = font_move_count.render("Moves: {}".format(num_moves), True, (0,0,0)) # (text, antialias, color)
		textRect_move_count = text_move_count.get_rect()  
		textRect_move_count.midleft = (50, size_window[1] - 25)
		window.blit(text_move_count, textRect_move_count)

		# Min moves
		font_move_min = pygame.font.Font('freesansbold.ttf', 24) 
		text_move_min = font_move_min.render("Moves to solve: {}".format(board.maze_key["sol_length"]), True, (0,0,0)) # (text, antialias, color)
		textRect_move_min = text_move_min.get_rect()  
		textRect_move_min.midright = (size_window[0] - 50, size_window[1] - 25)
		window.blit(text_move_min, textRect_move_min)

	# Begin token animation
	# Move player token first. 
	for frame in range(1, frames + 1):
		# Fill screen with white. This will allow everything to be redrawn.
		window.fill((255,255,255))

		draw_walls()

		# Draw Minotaur
		# Get coordinates of Minotaur
		mino_window_location = adj_token_coordinates(mino_moves[-3])
		pygame.draw.circle(surface = window, color = (255,0,0), center = mino_window_location, radius = int((tile_size_scaled*0.8)/2))

		# Annimate Player
		# Get coordinates of Player
		player_window_location_before = adj_token_coordinates(player_moves[-2])
		player_window_location_after = adj_token_coordinates(player_moves[-1])
		player_window_location_current = get_animation_pos(player_window_location_before, player_window_location_after, frame, frames)
		pygame.draw.circle(surface = window, color = (0,0,255), center = player_window_location_current, radius = int((tile_size_scaled*0.7)/2))

		# Draw Goal
		# Get coordinates of Goal
		goal_window_location = adj_token_coordinates(board.G.graph["goal"])
		pygame.draw.circle(surface = window, color = (0,255,0), center = goal_window_location, radius = int((tile_size_scaled*0.5)/2))

		draw_text(display_win_message)

		# Push Updates to window
		pygame.display.update()

		# FPS
		pygame.time.delay(int(1000/fps))
	# Next, animate minotaur token. 
	# Check if minotaur has even moved. 
	for i in range(2):
		if mino_moves[i-3] != mino_moves[i-2]:
			# Then mino has moved, draw animation. 
			for frame in range(1, frames + 1):
				# Fill screen with white. This will allow everything to be redrawn.
				window.fill((255,255,255))

				draw_walls()

				# Animate Minotaur
				# Get coordinates of Minotaur
				mino_window_location_before = adj_token_coordinates(mino_moves[i-3])
				mino_window_location_after = adj_token_coordinates(mino_moves[i-2])
				mino_window_location_current = get_animation_pos(mino_window_location_before, mino_window_location_after, frame, frames)
				pygame.draw.circle(surface = window, color = (255,0,0), center = mino_window_location_current, radius = int((tile_size_scaled*0.8)/2))

				# Draw Player
				# Get coordinates of Player
				player_window_location = adj_token_coordinates(player_moves[-1])
				pygame.draw.circle(surface = window, color = (0,0,255), center = player_window_location, radius = int((tile_size_scaled*0.7)/2))

				# Draw Goal
				# Get coordinates of Goal
				goal_window_location = adj_token_coordinates(board.G.graph["goal"])
				pygame.draw.circle(surface = window, color = (0,255,0), center = goal_window_location, radius = int((tile_size_scaled*0.5)/2))

				draw_text(display_win_message)

				# Push Updates to window
				pygame.display.update()

				# FPS
				pygame.time.delay(int(1000/fps))
		else: 
			# Fill screen with white. This will allow everything to be redrawn.
			window.fill((255,255,255))

			draw_walls()

			# Draw Minotaur
			# Get coordinates of Minotaur
			mino_window_location = adj_token_coordinates(mino_moves[i-3])
			pygame.draw.circle(surface = window, color = (255,0,0), center = mino_window_location, radius = int((tile_size_scaled*0.8)/2))

			# Draw Player
			# Get coordinates of Player
			player_window_location = adj_token_coordinates(player_moves[-1])
			pygame.draw.circle(surface = window, color = (0,0,255), center = player_window_location, radius = int((tile_size_scaled*0.7)/2))

			# Draw Goal
			# Get coordinates of Goal
			goal_window_location = adj_token_coordinates(board.G.graph["goal"])
			pygame.draw.circle(surface = window, color = (0,255,0), center = goal_window_location, radius = int((tile_size_scaled*0.5)/2))

			draw_text(display_win_message)

			# Push Updates to window
			pygame.display.update()

	draw_text(display_win_message = True)

	# Push Updates to window
	pygame.display.update()


# Set window size
window = pygame.display.set_mode(size = calculate_screen_size(maze)[0])
# window.fill((255,255,255)) # Fills the screen with white
# pygame.display.update()
pygame.display.set_caption("Minotaur Project")

run = True
draw = True
game_end = False
while run:
	# pygame.time.delay(10) # Wait 10 ms between cycles. 

	# Get keyboard press events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN and not game_end:
			# Get KEYDOWN so that holding a key will not trigger repeated movements.
			if event.key == pygame.K_w or event.key == pygame.K_UP:
				# Up
				try: 
					player_moves.append(player.move("up"))
					mino_moves.extend(mino.move()[1])
					draw = True
				except ValueError: 
					pass
			if event.key == pygame.K_a or event.key == pygame.K_LEFT:
				# Move left
				try: 
					player_moves.append(player.move("left"))
					mino_moves.extend(mino.move()[1])
					draw = True
				except ValueError: 
					pass
			if event.key == pygame.K_s or event.key == pygame.K_DOWN:
				# Down
				try: 
					player_moves.append(player.move("down"))
					mino_moves.extend(mino.move()[1])
					draw = True
				except ValueError: 
					pass
			if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
				# Right
				try: 
					player_moves.append(player.move("right"))
					mino_moves.extend(mino.move()[1])
					draw = True
				except ValueError: 
					pass
			if event.key == pygame.K_SPACE:
				# Skip
				try: 
					player_moves.append(player.move("skip"))
					mino_moves.extend(mino.move()[1])
					draw = True
				except ValueError: 
					pass
			if event.key == pygame.K_BACKSPACE:
				# Reset board
				maze.G.graph["player_location"] = player_moves[0]
				maze.G.graph["mino_location"] = mino_moves[0]
				player = Player(maze)
				mino = Minotaur(maze)
				player_moves = [maze.G.graph["player_location"], maze.G.graph["player_location"]]
				mino_moves = [maze.G.graph["mino_location"], maze.G.graph["mino_location"], maze.G.graph["mino_location"]]
				draw = True
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				# Undo move
				maze.G.graph["player_location"] = player_moves[-2]
				maze.G.graph["mino_location"] = mino_moves[-3]
				player = Player(maze)
				mino = Minotaur(maze)
				player_moves.append(player_moves[-2])
				mino_moves.extend([mino_moves[-2], mino_moves[-3]])
				draw = True
			if event.key == pygame.K_p:
				# View solution
				# Reset board 
				maze.G.graph["player_location"] = player_moves[0]
				maze.G.graph["mino_location"] = mino_moves[0]
				player = Player(maze)
				mino = Minotaur(maze)
				player_moves = [maze.G.graph["player_location"], maze.G.graph["player_location"]]
				mino_moves = [maze.G.graph["mino_location"], maze.G.graph["mino_location"], maze.G.graph["mino_location"]]
				draw = True
				# Redraw window
				if draw:
					draw_board(maze, window, player_moves, mino_moves, win_message)
					draw = False
				# Animate solution
				for move in maze.maze_key["solution"]:
					player_moves.append(player.move(move))
					mino_moves.extend(mino.move()[1])
					game_end, game_win = maze.check_win_condition()
					if game_end and game_win:
						win_message = "SOLUTION GIVEN"
					else:
						win_message = "Solving..."
						display_win_message = True
					draw_board(maze, window, player_moves, mino_moves, win_message, display_win_message)
					pygame.time.delay(100)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				# Reset board
				maze.G.graph["player_location"] = player_moves[0]
				maze.G.graph["mino_location"] = mino_moves[0]
				player = Player(maze)
				mino = Minotaur(maze)
				player_moves = [maze.G.graph["player_location"], maze.G.graph["player_location"]]
				mino_moves = [maze.G.graph["mino_location"], maze.G.graph["mino_location"], maze.G.graph["mino_location"]]
				draw = True
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				# Undo move
				maze.G.graph["player_location"] = player_moves[-2]
				maze.G.graph["mino_location"] = mino_moves[-3]
				player = Player(maze)
				mino = Minotaur(maze)
				player_moves.append(player_moves[-2])
				mino_moves.extend([mino_moves[-2], mino_moves[-3]])
				draw = True
	
	game_end, game_win = maze.check_win_condition()
	if game_end and game_win:
		win_message = "YOU WIN!"
	elif game_end and not game_win:
		win_message = "YOU LOSE!"
	else:
		win_message = " "

	# Redraw window
	if draw:
		draw_board(maze, window, player_moves, mino_moves, win_message)
		draw = False
	
pygame.quit()