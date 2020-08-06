from board_class import Board
from file_io import get_maze_key_from_file, write_dict_to_file, read_dict_from_file, write_set_to_file
import matplotlib.pyplot as plt

maze = Board()
print("\n")
num_sol_gen = {}

num_of_mazes_per_iter = 1
iterations = 1

for i in range(iterations):
	maze_set = maze.build_random_maze2(num_of_mazes=num_of_mazes_per_iter, verbose= True, size_board=(7,5), min_moves=20, adl_checks = False, adl_check_threshold = 8)
	print("\n")

	write_set_to_file(maze_set)

	print("\n")
	for key, value in sorted(maze_set.items()):
		num_sol_gen[key] = len(value)
	print("This pass generated these mazes: ")
	print(num_sol_gen)
	print("\n")

# Generate the histogram. 
keys = num_sol_gen.keys()
values = num_sol_gen.values()

plt.bar(keys, values)
plt.show()