from board_class import Board, Minotaur, Player
import file_io

# maze_key = file_io.read_dict_from_file("mazes/6x6.txt")[47][0]
maze_key = {'size_board': (5, 5), 'walls': [((0, 1), (1, 1)), ((1, 0), (1, 1)), ((1, 1), (1, 2)), ((1, 2), (2, 2)), ((1, 3), (1, 4)), ((2, 2), (2, 3)), ((2, 3), (2, 4)), ((3, 0), (3, 1)), ((3, 1), (3, 2)), ((3, 2), (3, 3)), ((3, 3), (3, 4)), ((4, 0), (4, 1)), ((4, 1), (4, 2)), ((4, 3), (4, 4))], 'player_start': (1, 4), 'mino_start': (4, 4), 'goal': (4, 4), 'solution': ['left', 'up', 'right', 'right', 'right', 'right', 'up', 'left', 'left', 'up', 'up', 'left', 'left', 'right', 'right', 'down', 'down', 'right', 'right', 'down', 'up', 'left', 'left', 'up', 'up', 'right', 'right', 'left', 'left', 'left', 'left', 'down', 'down', 'down', 'down', 'right', 'right', 'right', 'right'], 'sol_length': 39, 'seed': 7188903436156103517}
maze = Board(maze_key)

player = Player(maze)
mino = Minotaur(maze)

maze.visualize_board()

solution = maze_key["solution"]

game_end = False
moves = 0

for step in solution:
	# Get player move
	player_move = step

	# Update player location
	location_before = player.location
	player.move(player_move)
	location_after = player.location
	print("Player moved from {before} to {after}.".format(before=location_before, after=location_after))
	maze.visualize_board()

	moves += 1

	# Minotaur's turn
	location_before = mino.location
	mino.move()
	location_after = mino.location
	print("Minotaur moved from {before} to {after}.".format(before=location_before, after=location_after))
	maze.visualize_board()

	# Check win condition
	game_end, game_win = maze.check_win_condition()

if game_win:
	print("CONGRADULATIONS! You escaped the Minotaur in {} moves!".format(moves))
else:
	print("YOU LOSE!")
