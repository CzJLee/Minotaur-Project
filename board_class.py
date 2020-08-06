import networkx as nx
from visualize import visualize
from file_io import get_maze_key_from_file, write_dict_to_file, read_dict_from_file
from visualize2 import visualize2
import random
import sys
import copy
from collections import defaultdict
import random

class Board:
	def __init__(self, maze_key = None, maze_file = None, size_board = (5,5), seed = None):
		# maze_file should be a string of a .txt file in the same directory.
		if maze_key:
			self.maze_key = maze_key
			self.G = self.build_maze(self.maze_key)
			if not self.validate_maze(self.G):
				# Raise Error
				pass
		elif maze_file:
			try:
				self.maze_key = get_maze_key_from_file(maze_file)
				if self.maze_key:
					self.G = self.build_maze(self.maze_key)
					if not self.validate_maze(self.G):
						# Raise Error
						pass
				else:
					raise ValueError
			except FileNotFoundError:
				print("File is not found. Maze not generated.")
				exit()
		else:
			# Build random maze
			self.G, self.maze_key = self.build_random_maze(size_board = size_board, seed = seed)

		# Add move options to nodes
		self.add_move_options()

	def player_location(self):
		return self.G.graph["player_location"]

	def mino_location(self):
		return self.G.graph["mino_location"]

	def goal_location(self):
		return self.G.graph["goal"]

	def build_maze(self, maze_key, verbose = False):
		# maze_key should be a dictionary with attributes "size_board", "walls", "player_start", "mino_start", and "goal"
		# Return a NetworkX type graph object

		size_board = maze_key["size_board"] #[x, y] where x >= 2, y >= 2.

		# Generate board Graph. 
		G = nx.grid_2d_graph(*size_board)

		# Add size attribute
		G.graph['size_board'] = size_board

		# Add player location attribute
		G.graph["player_location"] = maze_key["player_start"]

		# Add mino location attribute
		G.graph["mino_location"] = maze_key["mino_start"]

		# Add goal locaton attribute
		G.graph["goal"] = maze_key["goal"]

		# Set all edge weights to 0. 
		G.add_edges_from(G.edges, weight = 0)

		# Set walls to have edge weight -1.
		walls = maze_key["walls"]
		G.add_edges_from(walls, weight = -1)

		if verbose:
			print(maze_key)

		return G

	def build_random_maze(self, size_board = (4,4), seed = None, verbose = False):
		if seed is None:
			seed = random.randrange(sys.maxsize)
		
		random.seed(seed)

		num_edges = (size_board[0] * (size_board[1] - 1)) + ((size_board[0] - 1) * size_board[1])
		# num_edges are the number of edges in a graph produced by size_board. 
		expected_number_walls = num_edges / 2
		wall_threshold = expected_number_walls / num_edges
		# If random number is < wall_threshold, then build a wall along that edge.

		# Generate board Graph. 
		G = nx.grid_2d_graph(*size_board)

		# Add size attribute
		G.graph['size_board'] = size_board

		attempts_wall = 0
		attempts_tokens = 0
		# attempts_valid = 0
		# attempts_min_moves = 0

		# Generate Walls
		is_valid_maze = False
		while is_valid_maze is False:
			attempts_wall += 1
			for edge in G.edges:
				if random.random() < wall_threshold:
					# Set edge weight to -1
					G.edges[edge]["weight"] = -1
				else:
					G.edges[edge]["weight"] = 0

			# Validate no loops
			is_valid_maze = self.validate_maze(G)
		
		# Add player start, mino start, and goal. 
		is_valid_maze = False
		while is_valid_maze is False:
			attempts_tokens += 1
			G.graph["player_location"] = random.choice(list(G.nodes))
			G.graph["mino_location"] = random.choice(list(G.nodes))
			G.graph["goal"] = random.choice(list(G.nodes))

			if G.graph["player_location"] == G.graph["goal"] or G.graph["player_location"] == G.graph["mino_location"]:
				is_valid_maze = False
			else:
				is_valid_maze = True

		print("Wall generation attempts: " + str(attempts_wall))
		print("Token generation attempts: " + str(attempts_tokens))

		# maze_key should be a dictionary with attributes "size_board", "walls", "player_start", "mino_start", and "goal"
		maze_key = {}
		maze_key["size_board"] = size_board
		maze_key["walls"] = [edge for edge in G.edges if G.edges[edge]["weight"] == -1]
		maze_key["player_start"] = G.graph["player_location"]
		maze_key["mino_start"] = G.graph["mino_location"]
		maze_key["goal"] = G.graph["goal"]
		maze_key["seed"] = seed

		if verbose:
			print(maze_key)
		
		return G, maze_key

	def build_random_maze2(self, size_board = (5,5), seed = None, min_moves = -1, num_of_mazes = 1000, adl_checks = True, adl_check_threshold = 0, verbose = False):
		# Second version of build_random_maze
		# The main goal of this version is to improve the speed of large map generation
		# The main problem with v1 is that the method of choosing random walls and then checking if the graph is connected is really inefficient. 
		# This uses a method of adding edges instead of removing them. 
		# Additonally, I would like to test multiple different player start, mino start, and goal locations on each wall config, as it appears that checking for solutions is fast compared to maze generation. 
		# Finally, I would like to return a dict object with a whole bunch of maze_keys rather than just a single maze. Instead of tossing all of the generated mazes that don't meet the criteria, I can choose to save them if I wish. 
		# If a maze is found with a sol len of less than min_moves, do not add it to the dictionary, and do not count it. This eliminates returning trivial mazes. 

		if seed is None:
			seed = random.randrange(sys.maxsize)
		
		random.seed(seed)

		if min_moves == -1:
			min_moves = max([size_board[0],size_board[1]])

		num_edges = (size_board[0] * (size_board[1] - 1)) + ((size_board[0] - 1) * size_board[1])
		# num_edges are the number of edges in a graph produced by size_board. 

		maze_set = defaultdict(list)
		num_of_mazes_generated = 0
		num_of_mazes_checked = 0
		num_of_boards_checked = 0
		largest_solution = 0
		additional_found = 0
		# https://docs.python.org/3/library/collections.html#collections.defaultdict
		# Using the first example to handle the maze dictionary. 
		# maze_set is a dict with keys equal to the solution length, and values is a list containing the different maze_keys. By using a default dict, if there does not already exist a maze_key with a particular number of moves, it will create the key. Else, it will append. 

		# Repeat maze generation until num_of_mazes_generated >= num_of_mazes
		while num_of_mazes_generated < num_of_mazes:
			# Generate board Graph. 
			G = nx.grid_2d_graph(*size_board)
			num_of_boards_checked += 1

			# Add graph attributes
			G.graph["player_location"] = (0,0)
			G.graph["mino_location"] = (1,1)
			G.graph["goal"] = (0,1)
			G.graph["size_board"] = size_board

			# Set every edge weight to -1. This is equivalent to having no edges and only nodes. 
			G.add_edges_from(G.edges, weight = -1)

			# Randomly change edges of weight -1 to 0 and check if the graph is connected. 
			# A graph needs a minimum of n-1 edges to be connected, where n is the number of nodes. 
			# After a graph is shown to be connected, it does not need to be checked again, as adding more edges will never disconnect it.
			list_of_edges = list(G.edges(data=True)) 
			for i in range((size_board[0]*size_board[1])):
				node1, node2, weight = list_of_edges.pop(random.choice(range(len(list_of_edges) - 1)))
				edge = (node1, node2)
				G.edges[edge]["weight"] = 0
			while not self.validate_maze(G):
				node1, node2, weight = list_of_edges.pop(random.choice(range(len(list_of_edges) - 1)))
				edge = (node1, node2)
				G.edges[edge]["weight"] = 0
			# At this point, all graphs are connected. 
			# Start adding in random player_start, mino_start, and goal. Then check if solvable. 
			# Test n different start configs where n = len(list_of_edges)

			while len(list_of_edges) > max([size_board[0],size_board[1]]):
				# Loop through adding edges, but stop when the number of walls left is equal to the largest dimension of the board. At this point, all mazes will be trivial.
				num_token_positions_to_check = len(list_of_edges)
				while num_token_positions_to_check > 0:
					# Add player start, mino start, and goal. 
					is_valid_maze = False
					while is_valid_maze is False:
						G.graph["player_location"] = random.choice(list(G.nodes))
						G.graph["mino_location"] = random.choice(list(G.nodes))
						G.graph["goal"] = random.choice(list(G.nodes))

						if G.graph["player_location"] == G.graph["goal"] or G.graph["player_location"] == G.graph["mino_location"]:
							is_valid_maze = False
						else:
							is_valid_maze = True

					num_token_positions_to_check -= 1

					# Build maze_key
					# maze_key should be a dictionary with attributes "size_board", "walls", "player_start", "mino_start", and "goal"
					maze_key = {}
					maze_key["size_board"] = size_board
					maze_key["walls"] = [edge for edge in G.edges if G.edges[edge]["weight"] == -1]
					maze_key["player_start"] = G.graph["player_location"]
					maze_key["mino_start"] = G.graph["mino_location"]
					maze_key["goal"] = G.graph["goal"]

					# Check if solvable
					if verbose:
						num_of_mazes_checked += 1
						print("Checking Board #{board} \t Maze #{maze} \t Adl. Checks: {adl} \t Total Mazes Generated: {generated} \t Largest Solution Length: {sol} \t".format(board=num_of_boards_checked, maze=num_of_mazes_checked, adl = num_token_positions_to_check if num_token_positions_to_check > len(list_of_edges) else 0 , generated = num_of_mazes_generated, sol=largest_solution), end="\r")
					is_solvable, solution = solve_key(maze_key)
					if is_solvable:
						# Maze is solvable
						len_sol = len(solution)
						if len_sol >= min_moves:
							# Add solution to maze_key
							maze_key["solution"] = solution[:]
							maze_key["sol_length"] = len(solution)
							maze_key["seed"] = seed
							maze_set[len_sol].append(maze_key)
							num_of_mazes_generated += 1
							if len_sol >= largest_solution:
								largest_solution = len_sol
								if num_token_positions_to_check > len(list_of_edges):
									additional_found += 1
								# Add in more checks on the same board if a new longest solution is found. 
								# If a new longest solution is found, there is a chance that the board has a good wall lay out. So try more tests with different token starting positions. 
								# I guess I will add an ammount proportional to largest_solution
								# For reference, a 5x5 board has 14,400 possible token arrangements. 
								if adl_checks and largest_solution >= adl_check_threshold:
									num_token_positions_to_check += int(largest_solution ** 2)

				# After that wall config has been tested, remove a wall/add an edge and try again. 
				node1, node2, weight = list_of_edges.pop(random.choice(range(len(list_of_edges) - 1)))
				edge = (node1, node2)
				G.edges[edge]["weight"] = 0

			# Clear all attributes, nodes, and edges from G to start with a new board. 
			G.clear()
			seed += 1
		
		if verbose:
			print("\n")
			print("{} mazes have been generated.".format(num_of_mazes_generated))
			print("The longest solution found had length {}.".format(sorted(maze_set.keys())[-1]))
			print("Additional Mazes Found: {}".format(additional_found))
		return dict(maze_set)

	def remove_wall_edges(self, maze):
		# Return a Graph object with the edges with attribute "weight" == -1 removed. 

		if "weight" in maze.edges[list(maze.edges)[0]]:
			# The passed maze graph has weight attributes on its edges. Need to remove those edges. 
			walls = [edge for edge in maze.edges if maze.edges[edge]["weight"] == -1]
			maze_remove_wall_edges = copy.deepcopy(maze)
			maze_remove_wall_edges.remove_edges_from(walls)

		return maze_remove_wall_edges

	def validate_maze(self, maze):
		# Returns true if the maze has no closed off sections. This is true if the graph is connected. 
		
		# Need to remove edges of weight -1 if the edges have weight attributes
		maze_remove_wall_edges = self.remove_wall_edges(maze)

		return nx.is_connected(maze_remove_wall_edges)

	def add_move_options(self):
		# Add node attributes to each node indicating the direction the player can possibly move in. An option is only not present if that path is blocked by a wall. 

		# Work with graph that shows node connections
		reference = self.remove_wall_edges(self.G)

		# Add "skip" as an option to every node. 
		for node in self.G.nodes:
			self.G.nodes[node]["options"] = ["skip"]
			# print(type(node))

			# Get list of nodes connected to node
			connected_nodes = nx.neighbors(reference, node)
			
			for neighbor in connected_nodes:
				if neighbor == (node[0] + 1, node[1] + 0):
					self.G.nodes[node]["options"].append("right")
				elif neighbor == (node[0] - 1, node[1] + 0):
					self.G.nodes[node]["options"].append("left")
				elif neighbor == (node[0] + 0, node[1] - 1):
					self.G.nodes[node]["options"].append("up")
				elif neighbor == (node[0] + 0, node[1] + 1):
					self.G.nodes[node]["options"].append("down")

		# self.node_attributes()

	def get_move_options(self, node = None):
		# Return a dict containing the move options for the player location and minotaur location
		move_options = {}
		if node:
			# Return the move options of the passed node instead. 
			# Return a list instead of dict
			move_options["player"] = self.G.nodes[node]["options"]
			move_options["mino"] = self.G.nodes[node]["options"][1:]
			return move_options
		
		player_location = self.player_location()
		mino_location = self.mino_location()
		move_options["player"] = self.G.nodes[player_location]["options"]
		move_options["mino"] = self.G.nodes[mino_location]["options"][1:]

		return move_options

	def print_node_attributes(self):
		print("\n")
		print("Node Attributes:")
		for node in self.G.nodes.data():
			print(node)

	def print_edge_attributes(self):
		print("\n")
		print("Edge Attributes:")
		for edge in self.G.edges.data():
			print(edge)

	def check_win_condition(self):
		# Return game_end, game_win. 
		# Return game_end = True if the player has reached the goal or encountered the minotaur. 
		# Return game_win = True if the player successfully reached the goal. 

		if self.G.graph["mino_location"] == self.G.graph["player_location"]:
			# Player Loses
			return True, False
		elif self.G.graph["player_location"] == self.G.graph["goal"] and self.G.graph["mino_location"] != self.G.graph["player_location"]:
			# Players Wins
			return True, True
		else:
			# Game is not over yet
			return False, False

	def visualize_board(self):
		visualize2(self.G)


class Minotaur:
	def __init__(self, maze):
		self.maze = maze
		self.location = maze.G.graph["mino_location"]

	def move(self):
		# Return new coordinates that the Minotaur will move to
		mino_location = self.maze.G.graph["mino_location"]
		player_location = self.maze.G.graph["player_location"]

		# MINOTAUR MOVEMENT RULESET
		# The Minotaur will always choose to move closer to the player. 
		# The Mintoaur will never move away from the player. 
		# If the Minotaur is not able to move closer to the player, it does not move at all.
		# The minotaur can move up to two spaces each turn.
		# The Minotaur always prioritizes horizontal movement over vertical. If the Minotaur can move horizontally to get closer to the player, it will continue to do so until it is in the same column as the player. 
		# If the Minotaur is unable to move horizontally, then it will move vertically. 
		# After moving vertically once, it will then check if it is able to move horizontally. 
		
		remaining_moves = 2
		move_to = []

		while remaining_moves > 0:
			# print("Current Minotaur Location: " + str(mino_location))
			# print("Current Player Location: " + str(player_location))

			# print("Move options: " + str(self.maze.get_move_options()["mino"]))

			move_options = self.maze.get_move_options()["mino"]


			# Check right
			if "right" in move_options and player_location[0] > mino_location[0]:
				# print("Minotaur can move right.")
				# Update mino_location
				mino_location = (mino_location[0] + 1, mino_location[1] + 0)
				move_to.append(mino_location)
			#Check left
			elif "left" in move_options and player_location[0] < mino_location[0]:
				# print("Minotaur can move left.")
				# Update mino_location
				mino_location = (mino_location[0] - 1, mino_location[1] + 0)
				move_to.append(mino_location)
			# Check up
			elif "up" in move_options and player_location[1] < mino_location[1]:
				# print("Minotaur can move up.")
				# Update mino_location
				mino_location = (mino_location[0] + 0, mino_location[1] - 1)
				move_to.append(mino_location)
			# Check down
			elif "down" in move_options and player_location[1] > mino_location[1]:
				# print("Minotaur can move down.")
				# Update mino_location
				mino_location = (mino_location[0] + 0, mino_location[1] + 1)
				move_to.append(mino_location)
			else:
				# print("Minotaur can not move.")
				move_to.append(mino_location)
			
			# If the Minotaur is not able to horizontally or vertically, then it can't move. 
			remaining_moves -= 1

			# Push update mino_location in maze. 
			self.maze.G.graph["mino_location"] = mino_location

		# When while loop has finished, the minotaur has completed its turn. 
		# Return mino_location

		self.location = mino_location
		return mino_location, move_to

class Player:
	def __init__(self, maze):
		self.maze = maze
		self.location = maze.G.graph["player_location"]
	
	def move(self, direction):
		if direction not in self.maze.get_move_options()["player"]:
			raise ValueError(str(direction) + " is not a valid direction.")
		else:
			player_location = self.maze.G.graph["player_location"]

			if direction == "skip":
				# Do not change player location
				pass
			elif direction == "right":
				player_location = (self.location[0] + 1, self.location[1] + 0)
			elif direction == "left":
				player_location = (self.location[0] - 1, self.location[1] + 0)
			elif direction == "up":
				player_location = (self.location[0] + 0, self.location[1] - 1)
			elif direction == "down":
				player_location = (self.location[0] + 0, self.location[1] + 1)
		
		# Push update player_location in maze. 
		self.maze.G.graph["player_location"] = player_location
	
		# Return player_location
		self.location = player_location
		return player_location

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

def solve_key(maze_key_to_solve):
	# Variation on solve that takes in a maze_key instead of a Board object, so that it will work within the board class. 

	# Breadth First Search algorithm to solve the Minotaur puzzle. 
	# https://en.wikipedia.org/wiki/Breadth-first_search
	# maze is the puzzle to be solved, and should be from the Board class. 
	# Return a bool and a list. True if the maze is solvable, and False if it is not. 
	# The list contains the sequence of player moves to solve the puzzle if True, or empty if False. 

	# Make deep copy of maze_to_solve to not disturb its current state
	# maze = copy.deepcopy(maze_to_solve)
	maze = Board(maze_key=maze_key_to_solve)

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

def gen_random_solvable_maze(size_board = (5,5), min_moves = 10, seed = None):
	is_solvable = False
	solution = []
	attempts = 0

	while is_solvable is False or len(solution) < min_moves:
		maze = Board(size_board = size_board, seed = seed)
		is_solvable, solution = solve(maze)
		attempts += 1
		seed = random.randrange(sys.maxsize) if seed == None else seed + 1
		if is_solvable and len(solution) >= min_moves:
			return maze, solution, attempts

