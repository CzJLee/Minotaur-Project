import pymongo
from pymongo import MongoClient
from re import fullmatch

# Connect to MongDB Atlas
username = "readonly"
password = "anwthgphkxZPjsTJaYgzWDpc8RNfN9ai"
client = MongoClient("mongodb+srv://minotaurproject.5tlzo.mongodb.net/", username = username, password = password)

# Connect to mazes database connection
db = client.mazes

def get_maze_from_db(size_board, sol_length):
	# Expect size_board to be a string in format "#x#" such as "5x5"
	if not fullmatch("\d+x\d+", size_board):
		raise Exception("size_board must be a string in format '#x#'.")
	elif not isinstance(sol_length, int) and sol_length > 0:
		raise Exception("sol_length must be a positive integer.")

	# Connect to collection
	collection = db[size_board]

	# Get one random document
	maze_cursor = collection.aggregate([
		{'$match': {'sol_length': sol_length}}, 
		{'$sample': {'size': 1}}
	])

	# Convert curser object to dict
	maze_dict = dict(list(maze_cursor)[0])

	# Check if dict_is empty
	if not maze_dict:
		raise Exception("No matches found")
	
	# maze_dict["walls"] must be a list of tuples
	maze_dict["walls"] = [(tuple(pair[0]), tuple(pair[1])) for pair in maze_dict["walls"]]

	# The following must be tuples, not lists
	convert_to_tuples = ["size_board", "player_start", "mino_start", "goal"]
	for key in convert_to_tuples:
		maze_dict[key] = tuple(maze_dict[key])

	return maze_dict

def get_sol_lengths(size_board):
	# Expect size_board to be a string in format "#x#" such as "5x5"
	if not fullmatch("\d+x\d+", size_board):
		raise Exception("size_board must be a string in format '#x#'.")

	# Connect to collection
	collection = db[size_board]

	# Get array of all unique elements
	return sorted(collection.distinct("sol_length"))

get_maze_from_db("5x5", 28)