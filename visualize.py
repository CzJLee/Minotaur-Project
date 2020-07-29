import matplotlib.pyplot as plt
import networkx as nx

def visualize(graph):
	g_strip_attr = nx.Graph()
	g_strip_attr.add_nodes_from(graph.nodes)
	g_strip_attr.add_edges_from(graph.edges)

	# write edgelist to grid.edgelist
	nx.write_edgelist(g_strip_attr, path="grid.edgelist", delimiter=":")
	# read edgelist from grid.edgelist
	H = nx.read_edgelist(path="grid.edgelist", delimiter=":")

	nx.draw(H)
	plt.show()

