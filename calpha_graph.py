import sys
from Queue import *
from random import *
import numpy
x=[];
z=[];
y=[];
names=[]
graphdict={}
randomgraphdict = {}
ints=[]
shortest_distance=[[0,1]]
clustering_coeff = []
random_graph2 = {}
#Adjacency matrix
adj_matrix = []
def get_coordinates(filename):
	f = open(filename,'r')
	count  = 0
	for lines in f.readlines():
		#print lines[12:14]
		if lines[0:4] == "ATOM" and lines[13:15] == "CA" and int(lines[23:26]) > count:
			count += 1
			x.append(float(lines[30:38]))
			y.append(float(lines[38:46]))
			z.append(float(lines[46:54]))
			names.append(str(lines[17:20]))
	for i in range(len(names)):
		ints.append(i+1)
	nodemap=dict(zip(ints,names))
	f.close()

def find_largest_component():
	pass

def compute_shortest_path(i,num_short_paths):
	queue = Queue()
	distance = []
	for j in range(len(names)+1):
		distance.append([-1,-2])
	distance[i][0] = 0
	queue.put(i)
	while (queue.qsize() != 0):
		node = queue.get()
		for j in graphdict[node]:
			if distance[j][0] == -1:
				distance[j][0] = distance[node][0] + 1
				distance[j][1] = node
				queue.put(j)
				if node != i:
					num_short_paths[node] += 1
	shortest_distance.append(distance)

def get_zero_matrix():
	matrix = [[0 for x in range(len(names))] for y in range(len(names))]
	return matrix


def get_adjacency_matrix(matrix):
	for i in graphdict.keys():
		for j in graphdict[i]:
			matrix[i-1][j-1] = 1
			matrix[j-1][i-1] = 1

def get_degree_matrix(matrix):
	for i in graphdict.keys():
		matrix[i-1][i-1] = len(graphdict[i])

def get_laplacian_matrix(matrix1, matrix2):
	return numpy.subtract(matrix1, matrix2)

def get_random_graph_2(graph):
	count = 0
	while count < 100:
		n1 = randint(1,len(names))
		n2 = randint(1,len(names))
		if n1 != n2:
			ind3 = randint(0,len(graph[n1])-1)
			ind4 = randint(0,len(graph[n2])-1)
			n3 = graph[n1][ind3]
			n4 = graph[n2][ind4]
			if n3 != n4:
				graph[n1].remove(n3)
				graph[n3].remove(n1)
				graph[n2].remove(n4)
				graph[n4].remove(n2)
				graph[n1].append(n4)
				graph[n4].append(n1)
				graph[n2].append(n3)
				graph[n3].append(n2)
				count += 1
	return graph


def betweenness(i,num_short_paths):
	if i <= len(names):
		return num_short_paths[i]

def shortest_path():
	ans = 0
	length = float(len(names))
	for i in range(1,len(names)+1):
		for j in range(i+1,len(names)+1):
			ans += shortest_distance[i][j][0]
	#Multiplying by 2 to match tool
	return 2*float(float(ans)/((length)*float((length-1))))

def distance(x1, y1, z1, x2, y2, z2):
	return float((((z2-z1)*(z2-z1)) + ((y2-y1)*(y2-y1)) +((x2-x1)*(x2-x1)))**(0.5))

def construct_graph():
	threshold = sys.argv[2]
	for i in range(len(names)):
		for j in range(len(names)):
			if i==j:
				continue;
			if distance(x[i],y[i],z[i],x[j],y[j],z[j]) <= float(threshold):
				add_edge(i+1,j+1)
				#print "yes"
	for i in range(1,len(names)):
		if i in graphdict.keys():
			if i+1 not in graphdict[i] and i+1 <= len(names):
				add_edge(i,i+1)
		else:
			graphdict[i] = [i+1]

def add_edge(i, j):
	if i in graphdict.keys():
		graphdict[i].append(j)
	else:
		graphdict[i] = [j]


def print_graph(nodemap):
	for i in range(len(names)+1):
		if i in graphdict.keys():
			print str(i) + "     "
			print graphdict[i]

def calculate_average_degree():
	degreesum = 0;
	for i in graphdict.keys():
		degreesum += len(graphdict[i])
	return float(float(degreesum)/float(len(x)))

def find_clustering_coeff(i):
	cnt = 0
	if i not in graphdict.keys():
		return
	length = len(graphdict[i])
	for nodes in graphdict[i]:
		for subnodes in graphdict[nodes]:
			if subnodes in graphdict[i]:
				cnt += 1
	if length > 1:
		clustering_coeff.append(float(float(cnt)/(float(length)*float(length-1))))

def average_clustering_coeff():
	total = 0
	for i in clustering_coeff:
		total += i
	n = len(names)
	return float(float(total)/float(n))

def find_number_edges():
	edges = 0
	for i in graphdict.keys():
		edges += len(graphdict[i])
	return edges/2

def calculate_degree_distribution(graph):
	deg_distribution = []
	for k in range(2,16):
		nodes = 0
		for i in graph.keys():
			if len(graph[i]) == k:
				nodes += 1
		deg_distribution.append(float(float(nodes)/float(len(names))))
	return deg_distribution

#Gives errors at some places
def calculate_clust_coeff_distribution(graph):
	clust_coeff_distr = []
	nodes = 0
	clust_coeff_sum = 0
	for k in range(2,16):
		for i in range(1,len(names)+1):
			if i in graph.keys():
				if len(graph[i]) == k:
					nodes += 1
					if i-1 < len(clustering_coeff):
						clust_coeff_sum += float(clustering_coeff[i-1])
		if nodes == 0:
			clust_coeff_distr.append(0)
		else:
			clust_coeff_distr.append(float(float(clust_coeff_sum)/float(nodes)))
	return clust_coeff_distr


def closeness(nodes_closeness):
	for i in range(1,len(names)+1):
		ans = 0
		for j in range(1,len(names)+1):
			if j != i:
				ans += shortest_distance[j][i][0]
		if ans == 0:
			nodes_closeness[i] = 0
		else:
			nodes_closeness[i] = float(float(1)/float(ans))

def construct_random_graph():
	num_nodes = len(names)
	num_edges = 0
	for i in graphdict.keys():
		num_edges += len(graphdict[i])
	edges = []
	edgecount = 0
	for i in graphdict.keys():
		randomgraphdict[i] = []
	for i in graphdict.keys():
		#num_edges = len(graphdict[i])
		#edgecount = len(randomgraphdict[i])
		while edgecount < num_edges:
			node1 = randint(1,len(names))
			node2 = randint(1,len(names))
			if node1 != node2 and node2 not in randomgraphdict[node1]:
				randomgraphdict[node1].append(node2)
				randomgraphdict[node2].append(node1)
				edgecount += 2
	#print randomgraphdict


def main():
	nodemap={}
	filename = sys.argv[1]
	get_coordinates(str(filename))
	construct_graph()
	print "generating random graph"
	construct_random_graph()
	print "\n\n\n"
	#To store the closeness centrality of each node
	nodes_closeness = []
	#To store the number of shortest paths passing through each vertex
	num_short_paths=[]
	#initialising list elements
	for i in range(len(names)+1):
		num_short_paths.append(0)
		nodes_closeness.append(0)
	#Computing shortest path for each node to all other nodes
	for i in range(1,len(names)+1):
		compute_shortest_path(i,num_short_paths)
	#print "num short path = " + str(num_short_paths)
	#print_graph(nodemap)
	print "nodes = " + str(len(names))
	print "average degree = " + str(calculate_average_degree())
	for i in range(len(names)+1):
		find_clustering_coeff(i+1)
	print "avg clustering coeff  = " + str(average_clustering_coeff())
	print "edges = " + str(find_number_edges())
	print "average shortest path = " + str(shortest_path())
	print "\n\n"
	"""print "Do you wish to calculate degree distribution?\nEnter 1 to calculate\n"
	deg_dist = input()
	if deg_dist == 1:
		print "degree dist = " + str(calculate_degree_distribution(graphdict))
		#print "degree dist for random graph = " + str(calculate_degree_distribution(randomgraphdict))
	print "Do you wish to calculate clustering coeff distribution?\nEnter 1 to calculate"
	deg_dist = input()
	if deg_dist == 1:
		print "clustering coeff dist = " + str(calculate_clust_coeff_distribution(graphdict))
		#print "clustering coeff dist for random graph = " + str(calculate_clust_coeff_distribution(randomgraphdict))
	print "Do you wish to display betweenness centrality of all nodes?\nPress 1 to print"
	deg_dist = input()
	if deg_dist == 1:
		print num_short_paths
	print "Do you wish to display closeness centrality of all nodes?\nPress 1 to print"
	deg_dist = input()
	if deg_dist == 1:
		closeness(nodes_closeness)
		print nodes_closeness
	print "\n\n\n"""
	#print graphdict"""
	adj_matrix = get_zero_matrix()
	deg_matrix = get_zero_matrix()
	get_adjacency_matrix(adj_matrix)
	get_degree_matrix(deg_matrix)
	lap_matrix = get_laplacian_matrix(deg_matrix, adj_matrix)
	adj_value,adj_vec =  numpy.linalg.eigh(adj_matrix)
	lap_value,lap_vec = numpy.linalg.eigh(lap_matrix)
	"""print "For adjacency matrix\nLargest eigen value = " + str(adj_value[len(names)-1])
	print "\nCorresponding eigen vector = " + str(adj_vec[len(names)-1])
	print "For laplacian matrix\nLargest eigen value = " + str(lap_value[len(names)-1])
	print "\nCorresponding eigen vector = " + str(lap_vec[len(names)-1])"""
	random_graph2 = graphdict.copy()
	random_graph2 = get_random_graph_2(random_graph2)
	print random_graph2



if __name__ == '__main__':
	main()
