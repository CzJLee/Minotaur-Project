import matplotlib.pyplot as plt
import matplotlib.axes
import numpy as np 
import networkx as nx
from matplotlib import collections
import warnings

warnings.filterwarnings("ignore")

# May I just add, that I absolutely hate matplotlib with a burning passion. What garbage. 

def visualize2(graph):
	# Graph is a Graph object from NetworkX. 
	# size_board is infered from Graph attributes. 
	wall_color = "black"
	wall_width = 5
	player_color = "blue"
	player_icon_size = 30
	mino_color = "red"
	mino_icon_size = 40
	goal_color = "green"
	goal_icon_size = 25

	size_board = graph.graph["size_board"]
	mino_location = graph.graph["mino_location"]
	player_location = graph.graph["player_location"]
	goal_location = graph.graph["goal"]

	# Show Grid Lines
	plt.grid(True)

	# Set bounding axis in the same format as array
	plt.axis([0, size_board[0], size_board[1], 0])

	# Set aspect ratio to be 1:1
	plt.axes().set_aspect('equal')

	# Set ticks to be 1 unit
	plt.xticks(list(range(int(plt.axis()[1])+1)))
	plt.yticks(list(range(int(plt.axis()[2])+1)))

	# Get wall edges. 
	walls = []
	for edge, weight in graph.edges.items():
		# print(weight)
		if weight["weight"] == -1:
			# print(edge)
			edge_as_list = []
			for node in edge:
				edge_as_list.append(list(node))
			walls.append(list(edge_as_list))

	# Convert list of walls to coordinate line segments. 
	# Walls are in format of ((x1, y1), (x2, y2))
	# Need to be in format of ((x1, x2), (y1, y2))
	# Also, the node corrdinates to not correspond to plot coordinates for walls. 
	# A wall is by an edge of weight -1 from one node to another node. The line segment that will represent the wall will be perpendicular to this. 

	# Given a edge ((x1, y1), (x2, y2)) that represents a wall, some modifications need to be done depending on if the wall is horizontal or vertical. 
	# If the wall is horizontal, then the new coordinate line segment is ((x1, y1 + 1), (x2 + 1, y2))
	# If the wall is vertical, then the new coordinate line segment is ((x1 + 1, y1), (x2, y2 + 1))
	# Some visual examples may need to be drawn to see why. 

	# A wall is horizontal if the original ((x1, y1), (x2, y2)) has abs(x2 - x1) == 0 and abs(y2 - y1) == 1
	# A wall is vertical if the original ((x1, y1), (x2, y2)) has abs(x2 - x1) == 1 and abs(y2 - y1) == 0

	# First step. Apply the proper conversion as outlined above. 
	# print(walls)
	for wall in walls:
		x1, y1 = wall[0]
		x2, y2 = wall[1]

		#Check if horizontal
		if abs(x2 - x1) == 0 and abs(y2 - y1) == 1:
			y1 += 1
			x2 += 1
		elif abs(x2 - x1) == 1 and abs(y2 - y1) == 0:
			x1 += 1
			y2 += 1
		else: 
			raise ValueError

		wall[0] = [x1, y1]
		wall[1] = [x2, y2]

	# print(walls)

	# Next step. Swap format from ((x1, y1), (x2, y2)) to ((x1, x2), (y1, y2))
	for wall in walls:
		x1, y1 = wall[0]
		x2, y2 = wall[1]

		y1, x2 = x2, y1

		wall[0] = [x1, y1]
		wall[1] = [x2, y2]

	# print(walls)

	# Create a separate plot element for each wall segment. 
	for wall in walls:
		plt.plot(wall[0], wall[1], color=wall_color, linewidth=wall_width)

	# Draw boarder bounding box
	# ((0,0), (0,y)) -> ((0,0), (0,y))
	# ((0,4), (4,4)) -> ((0,x), (y,y))
	# ((4,0), (4,4)) -> ((x,x), (0,y))
	# ((0,0), (4,0)) -> ((0,x), (0,0))
	x_max = size_board[0]
	y_max = size_board[1]
	# print(y_max)
	plt.plot((0,0), (0,y_max), color=wall_color, linewidth=wall_width)
	plt.plot((0,x_max), (y_max,y_max), color=wall_color, linewidth=wall_width)
	plt.plot((x_max,x_max), (0,y_max), color=wall_color, linewidth=wall_width)
	plt.plot((0,x_max), (0,0), color=wall_color, linewidth=wall_width)

	# Add in player, mino, and goal icons
	# Plot a single point with some attributes
	# If icon is at node (i, j) then it needs to be plotted at (i + 0.5, j + 0.5).
	plt.plot(mino_location[0] + 0.5, mino_location[1] + 0.5, marker='o', markersize=mino_icon_size, color=mino_color)
	plt.plot(player_location[0] + 0.5, player_location[1] + 0.5, marker='o', markersize=player_icon_size, color=player_color)
	plt.plot(goal_location[0] + 0.5, goal_location[1] + 0.5, marker='o', markersize=goal_icon_size, color=goal_color)

	plt.show()