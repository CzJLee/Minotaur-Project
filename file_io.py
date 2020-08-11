from os.path import isfile
import random

def get_maze_key_from_file(text_file):
	# Return list of edges, player location, mino location, and goal to be put into NetworkX .add_edges_from()
	# Return type is a dict known as maze_key
	# Text file input should be a string, the name of the text file. 
	# The text file should have each edge as a tuple separated by a new line
	# The last three lines are the player start, mino start, and goal location. 

	maze_key = {}
	with open(text_file, 'r') as f:
		maze_file = f.read().splitlines() 
		# print(maze_file)
		maze_key["size_board"] = eval(maze_file.pop(0)) # size_board is the first line
		maze_key["goal"] = eval(maze_file.pop())
		maze_key["mino_start"] = eval(maze_file.pop())
		maze_key["player_start"] = eval(maze_file.pop())
		# print(maze_file)
		maze_key["walls"] = [eval(edge) for edge in maze_file]
		return maze_key

def write_dict_to_file(d, text_file):
	with open(text_file, 'w') as f:
		print(d, file=f)

def read_dict_from_file(text_file):
	with open(text_file, "r") as f:
		d = f.read()
		return eval(d)

def write_set_to_file(d_set, min_length_trim = 0, verbose = True):
	# Get size_board from the first entry
	size_board = list(d_set.values())[0][0]["size_board"]
	file_dir = "mazes/{n}x{m}.txt".format(n=size_board[0], m=size_board[1])
	# print(file_dir)

	trim_d_set = {}
	for key, value in d_set.items():
		if key >= min_length_trim:
			trim_d_set[key] = value
	d_set = trim_d_set

	if isfile(file_dir):
		current_d_set = read_dict_from_file(file_dir)
		for key, value in current_d_set.items():
			if key in d_set:
				d_set[key] = list(d_set[key]) + list(value)
			else:
				d_set[key] = value
		# Sort dict
		sorted_d_set = {}
		for key, value in sorted(d_set.items(), reverse = True):
			sorted_d_set[key] = value
		# Write to file
		write_dict_to_file(sorted_d_set, file_dir)
	else:
		# Sort dict
		sorted_d_set = {}
		for key, value in sorted(d_set.items(), reverse = True):
			sorted_d_set[key] = value
		write_dict_to_file(sorted_d_set, file_dir)

	if verbose:
		num_sol_gen = {}
		for key, value in sorted(sorted_d_set.items()):
			num_sol_gen[key] = len(value)
		print("{file} has {num}".format(file=file_dir, num = num_sol_gen))

def print_maze_dict_size(text_file):
	maze_set = read_dict_from_file(text_file)
	num_sol = {}
	for key, value in sorted(maze_set.items()):
		num_sol[key] = len(value)
	print(num_sol)

	return num_sol

def get_maze(size = "random", difficulty = "random"):
	small_maze_files_to_source_from = ["4x4.txt", "5x5.txt", "3x5.txt", "4x3.txt", "5x3.txt", "5x4.txt"]
	medium_maze_files_to_source_from = ["6x6.txt", "7x7.txt", "7x5.txt"]
	large_maze_files_to_source_from = ["8x8.txt", "9x9.txt", "11x11.txt", "15x11.txt", "26x14.txt"]
	all_maze_files_to_source_from = small_maze_files_to_source_from + medium_maze_files_to_source_from + large_maze_files_to_source_from

	# size should be small, medium, large, random, or an item in all_maze_files_to_source_from.
	# difficulty should be easy, medium, hard, max, or random. 

	if size in all_maze_files_to_source_from:
		maze_file = size
	elif size in ["small", "medium", "large", "random"]:
		if size == "small":
			maze_file = random.choice(small_maze_files_to_source_from)
		elif size == "medium":
			maze_file = random.choice(medium_maze_files_to_source_from)
		elif size == "large":
			maze_file = random.choice(large_maze_files_to_source_from)
		elif size == "random":
			maze_file = random.choice(all_maze_files_to_source_from)
	
	maze_file = "mazes/{}".format(maze_file)

	print("Getting {} difficulty maze from {}...".format(difficulty, maze_file))
	maze_dict = read_dict_from_file(maze_file)
	maze_sizes = sorted(list(maze_dict.keys()))
	# easy, medium, and hard difficulty correspond to 1/3 of the maze_sizes key size. 
	if difficulty == "easy":
		maze_sizes = maze_sizes[:len(maze_sizes)//3]
		maze_size = random.choice(maze_sizes)
		maze_key = random.choice(maze_dict[maze_size])
	elif difficulty == "medium":
		maze_sizes = maze_sizes[len(maze_sizes)//3:2*len(maze_sizes)//3]
		maze_size = random.choice(maze_sizes)
		maze_key = random.choice(maze_dict[maze_size])
	elif difficulty == "hard":
		maze_sizes = maze_sizes[2*len(maze_sizes)//3:]
		maze_size = random.choice(maze_sizes)
		maze_key = random.choice(maze_dict[maze_size])
	elif difficulty == "max":
		maze_size = maze_sizes[-1]
		maze_key = random.choice(maze_dict[maze_size])
	elif difficulty == "random":
		maze_size = random.choice(maze_sizes)
		maze_key = random.choice(maze_dict[maze_size])
	
	return maze_key

def trim_maze_dict(trim_length, text_file):
	maze_dict = read_dict_from_file(text_file)

	print("Before: ")
	num_sol_before = {}
	total_before = 0
	for key, value in sorted(maze_dict.items()):
		num_sol_before[key] = len(value)
		total_before += len(value)
	print(num_sol_before)

	input_confirmation = input("Are you sure you would like to trim to {} on {}? Y/N: ".format(trim_length, text_file))
	
	if input_confirmation not in ["y", "Y", "yes", "YES"]:
		return
		# Return to not proceed. 

	new_maze_dict = {}
	for key, value in sorted(maze_dict.items()):
		if len(value) > trim_length:
			# Get a set of all seeds of all maze_keys in this list. Each seed is unique to a wall layout. Mazes with the same seed only differ in starting positions. Start by throwing out all duplicate seeds. 

			new_maze_key_list = []

			list_of_walls = set()
			for maze_key in value:
				if tuple(maze_key["walls"]) not in list_of_walls:
					list_of_walls.add(tuple(maze_key["walls"]))
					new_maze_key_list.append(maze_key)

			while len(new_maze_key_list) > trim_length:
				# If the list is still longer than trim_length, then randomly pick trim_length elements to include, and discard the rest. 
				index_to_remove = random.randrange(len(new_maze_key_list))
				new_maze_key_list.pop(index_to_remove)
		
			new_maze_dict[key] = new_maze_key_list
		
		else:
			# List is already below trim_length. In this case, just copy the kv pair. 
			new_maze_dict[key] = value

	print("After: ")
	num_sol = {}
	total_after = 0
	for key, value in sorted(new_maze_dict.items()):
		num_sol[key] = len(value)
		total_after += len(value)
	print(num_sol)	

	print("Removed {} maze_keys from {}".format(total_before - total_after, text_file))

	write_dict_to_file(new_maze_dict, text_file)

# trim_maze_dict(trim_length = 100, text_file = "mazes/11x11.txt")


