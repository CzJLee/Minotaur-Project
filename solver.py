from board_class import Board, Minotaur, Player
import copy

def solve(maze_to_solve):
	# Breadth First Search algorithm to solve the Minotaur puzzle. 
	# https://en.wikipedia.org/wiki/Breadth-first_search
	# maze is the puzzle to be solved, and should be from the Board class. 
	# Return a bool and a list. True if the maze is solvable, and False if it is not. 
	# The list contains the sequence of player moves to solve the puzzle if True, or empty if False. 

	# Make deep copy of maze_to_solve to not disturb its current state
	maze = copy.deepcopy(maze_to_solve)

	# Make a player and minotaur class
	player_solver = Player(maze)
	mino_solver = Minotaur(maze)

	# Initialize player_location, mino_location, and current_state
	player_location = player_solver.location
	mino_location = mino_solver.location
	current_state = (player_location, mino_location)

	# Queue will hold all of the moves to check. 
	# Queue also needs to hold the current state associated with the move. 
	# Each element in queue will have form [option, current_state, move_list], where current_state = (player_location, mino_location)
	# The search will end when the queue is empty. If it is empty, then all possible options have been exhausted and there is no solution. 
	move_queue = []
	# Initialize move_queue
	for option in maze.get_move_options(player_location)["player"]:
		move_queue.append([option, current_state, []])
	# print(move_queue)

	# Let visited be a set. All previous states will be stored in visited. A branch should terminate if its state is in visited. If the state is already in visited, then the player has gone in a loop, and the algorithm should not continue searching. 
	visited = set()

	while move_queue:
		# Get next item in queue
		option, current_state, move_list = move_queue.pop(0)
		player_location, mino_location = current_state
		# option = "left"
		# print("Option: {}".format(option))
		# print("Current State: {}".format(current_state))
		# print("Move List: {}".format(move_list))

		# Check if current_state is in visited. 
		if (option, current_state) in visited:
			# Then this option and this state has already been visited. The algorithm should not check it again. 
			continue
		
		# Add the current state to visited
		visited.add((option, current_state))

		# Apply current state to objects
		maze.G.graph["player_location"] = player_location
		maze.G.graph["mino_location"] = mino_location
		player_solver.location = player_location
		mino_solver.location = mino_location

		# Apply Player move
		player_location = player_solver.move(option)

		# Apply Mino move
		mino_location = mino_solver.move()[0]

		# print("After move, player location is {} and minotaur location is {}".format(maze.G.graph["player_location"], maze.G.graph["mino_location"]))
		
		# Check game condition
		game_end, game_win = maze.check_win_condition()

		if game_end is False:
			# The game continues. Add new options to queue. 
			# print("Continue game.")
			current_state = (player_location, mino_location)
			move_list.append(option)
			for new_option in maze.get_move_options(player_location)["player"]:
				move_queue.append([new_option, current_state, move_list[:]])
			pass
		elif game_end is True and game_win is False:
			# In this case, the Minotaur killed the player. No new options are added to the queue. 
			# print("Game loss.")
			pass
		elif game_end is True and game_win is True:
			# The solver has found a solution. 
			move_list.append(option)
			return True, move_list
		
		# maze.visualize_board()
		# print(move_queue)

	# If the end of the while loop is reached, then there is no solution. 
	return False, []



maze = Board(maze_file="mazes/level_20.txt")
maze.visualize_board()
print("\n")
solvable, solution = solve(maze)
if solvable:
	print("The maze is solvable in {} moves with the following solution: ".format(len(solution)))
	print(solution)
else:
	print("The maze is not solvable.")
maze.visualize_board()
