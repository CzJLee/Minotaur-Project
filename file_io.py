from os.path import isfile

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