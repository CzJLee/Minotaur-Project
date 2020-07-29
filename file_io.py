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

# print(get_maze_key_from_file("test_maze.txt"))
