import pymongo
from pymongo import MongoClient
import mongodb_atlas_credentials
import file_io

# Connect to MongDB Atlas
username = mongodb_atlas_credentials.rwusername
password = mongodb_atlas_credentials.rwpasssword
client = MongoClient("mongodb+srv://minotaurproject.5tlzo.mongodb.net/", username = username, password = password)

# Import list of all mazes in a set
maze_set = "26x14" # Edit this line
filename = "mazes/" + maze_set + ".txt"
print(f"Importing file {filename}...")
maze_dict = file_io.read_dict_from_file(filename)
print("Imported file " + filename)

# Create mazes database connection
db = client.mazes
# The collection names will be the maze_set name
collection = db[maze_set]

# Iterate over all mazes in the dict
# Dict structure has keys of the solution length, with a value of an array of maze_dicts. 
for sol_length, maze_array in maze_dict.items():
	# Use insert_many to insert the entire array of documents
	acknowledged = collection.insert_many(maze_array, ordered = False).acknowledged
	if acknowledged:
		print(f"Insertion of solution length {sol_length} from set {maze_set} successful.")
	else:
		print("Insertion failed.")