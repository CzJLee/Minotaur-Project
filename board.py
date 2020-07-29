import networkx as nx
from visualize import visualize
from file_io import get_edges_from_text
from visualize2 import visualize2

# Work with a 4x4 board right now. These contain the best examples.
size_board = [4, 4] #[x, y] where x >= 2, y >= 2.

# Generate board Graph. 
G = nx.grid_2d_graph(*size_board)

# Add size attribute
G.graph['size'] = size_board

# Set all edge weights to 0. 
G.add_edges_from(G.edges, weight = 0)

# Set walls to have edge weight -1.
walls = get_edges_from_text("test_maze.txt")
G.add_edges_from(walls, weight = -1)


# # Remove edge from G if there is a wall. This will create a graph of the possible board movements. 
# G.remove_edges_from(walls)

# for item in G.edges.items():
# 	print(item)

visualize2(G)