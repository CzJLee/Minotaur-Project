import networkx as nx
from visualize import visualize
from file_io import get_maze_key_from_file
from visualize2 import visualize2
import random
import sys
import copy

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

	def build_maze(self, maze_key):
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

		print(maze_key)

		return G

	def build_random_maze(self, size_board = (4,4), seed = None):
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

		print(maze_key)
		
		return G, maze_key

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
			#Check left
			elif "left" in move_options and player_location[0] < mino_location[0]:
				# print("Minotaur can move left.")
				# Update mino_location
				mino_location = (mino_location[0] - 1, mino_location[1] + 0)
			# Check up
			elif "up" in move_options and player_location[1] < mino_location[1]:
				# print("Minotaur can move up.")
				# Update mino_location
				mino_location = (mino_location[0] + 0, mino_location[1] - 1)
			# Check down
			elif "down" in move_options and player_location[1] > mino_location[1]:
				# print("Minotaur can move down.")
				# Update mino_location
				mino_location = (mino_location[0] + 0, mino_location[1] + 1)
			else:
				# print("Minotaur can not move.")
				pass
			
			# If the Minotaur is not able to horizontally or vertically, then it can't move. 
			remaining_moves -= 1

			# Push update mino_location in maze. 
			self.maze.G.graph["mino_location"] = mino_location

		# When while loop has finished, the minotaur has completed its turn. 
		# Return mino_location

		self.location = mino_location
		return mino_location

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
		mino_location = mino_solver.move()

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
