from board_class import Board, Minotaur, Player, gen_random_solvable_maze
from time import sleep

def get_player_move():
	player_move = input("Move: ")
	if player_move in ["u", "up"]:
		player_move = "up"
	elif player_move in ["d", "down"]:
		player_move = "down"
	elif player_move in ["l", "left"]:
		player_move = "left"
	elif player_move in ["r", "right"]:
		player_move = "right"
	elif player_move in ["s", "skip"]:
		player_move = "skip"
	return player_move

print("\n")
print("Theseus and the Minotaur")
print("\n")
sleep(0.1)

print("Loading Level...")
# maze = Board(maze_file="mazes/level_11.txt")
# maze = Board()
maze, solution, attempts = gen_random_solvable_maze(min_moves = 20, size_board=(4,5), seed = 4970200303410980824)
print("Maze generation attempts: " + str(attempts))
print("The maze is solvable in {} moves with the following solution: ".format(len(solution)))
print(solution)

player = Player(maze)
mino = Minotaur(maze)
print("Game Start!")

print("To move your character, please enter one of the following: 'up', 'down', 'left', 'right', or 'skip'.")
print("You are blue. Your goal is to get to the green dot. Avoid getting killed by the red Minotuar.")
maze.visualize_board()

game_end = False
moves = 0

while game_end is False:
	# Get player move
	player_move = get_player_move()

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

