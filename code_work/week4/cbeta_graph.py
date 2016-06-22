import sys
from Queue import *
from random import *
x=[];
z=[];
y=[];
names=[]
graphdict={}
randomgraphdict = {}
ints=[]
shortest_distance=[[0,1]]
clustering_coeff = []
def get_coordinates(filename):
	f = open(filename,'r')
	count  = 0
	for lines in f.readlines():
		#print lines[12:14]
		if lines[0:4] == "ATOM" and lines[13:15] == "CB" and int(lines[23:26]) > count:
			count += 1
			x.append(float(lines[30:38]))
			y.append(float(lines[38:46]))
			z.append(float(lines[46:54]))
			names.append(str(lines[17:20]))
	for i in range(len(names)):
		ints.append(i+1)
	nodemap=dict(zip(ints,names))
	f.close()

def compute_shortest_path(i):
	queue = Queue()
	distance = []
	for j in range(len(names)+1):
		distance.append([-1,-2])
	distance[i][0] = 0
	queue.put(i)
	while (queue.qsize() != 0):
		node = queue.get()
		if node in graphdict.keys():
			for j in graphdict[node]:
				if distance[j][0] == -1:
					distance[j][0] = distance[node][0] + 1
					distance[j][1] = node
					queue.put(j)
	shortest_distance.append(distance)

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
			"""if i == 0:
					print distance(x[i],y[i],z[i],x[j],y[j],z[j])"""
			if distance(x[i],y[i],z[i],x[j],y[j],z[j]) <= float(threshold):
				add_edge(i+1,j+1)
	for i in range(1,len(names)+1):
		if i in graphdict.keys():
			if i+1 not in graphdict[i] and i+1 <= len(names):
				add_edge(i,i+1)
		elif i+1 <= len(names):
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
		if nodes not in graphdict.keys():
			continue
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

def calculate_degree_distribution():
	k = input("Please enter the degree value")
	nodes = 0
	for i in graphdict.keys():
		if len(graphdict[i]) == k:
			nodes += 1
	return float(float(nodes)/float(len(names)))

def calculate_clust_coeff_distribution():
	k = input("Please enter the degree value")
	nodes = 0
	clust_coeff_sum = float(0)
	for i in graphdict.keys():
		if len(graphdict[i]) == k:
			nodes += 1
			clust_coeff_sum += float(clustering_coeff[i])
	return float(float(clust_coeff_sum)/float(nodes))

def closeness(nodes_closeness):
	for i in range(1,len(names)+1):
		ans = 0
		for j in range(1,len(names)+1):
			if j != i:
				ans += shortest_distance[j][i][0]
		nodes_closeness[i] = ans

def construct_random_graph():
	num_nodes = len(names)
	num_edges = 0
	for i in graphdict.keys():
		num_edges += len(graphdict[i])
	edges = []
	edgecount = 0
	for i in graphdict.keys():
		randomgraphdict[i] = []
	while edgecount < num_edges:
		node1 = randint(1,len(names))
		node2 = randint(1,len(names))
		if node1 != node2 and node2 not in randomgraphdict[node1]:
			randomgraphdict[node1].append(node2)
			randomgraphdict[node2].append(node1)
			edgecount += 2
	print randomgraphdict


def main():
	nodemap={}
	filename = sys.argv[1]
	get_coordinates(str(filename))
	construct_graph();
	for i in range(1,len(names)+1):
		compute_shortest_path(i)
	#print_graph(nodemap)
	print "average degree = " + str(calculate_average_degree())
	for i in range(len(names)+1):
		find_clustering_coeff(i+1)
	print "avg clustering coeff  = " + str(average_clustering_coeff())
	print "edges = " + str(find_number_edges())
	print "average shortest path = " + str(shortest_path())
	print "\n\n"
	print "Do you wish to calculate degree distribution?\nEnter 1 to calculate"
	deg_dist = input()
	if deg_dist == 1:
		print "degree dist = " + str(calculate_degree_distribution())
	print "Do you wish to calculate clustering coeff distribution?\nEnter 1 to calculate"
	deg_dist = input()
	if deg_dist == 1:
		print "clustering coeff dist = " + str(calculate_clust_coeff_distribution())
	print "Do you wish to display betweenness centrality of all nodes?\nPress 1 to print"
	deg_dist = input()
	if deg_dist == 1:
		print num_short_paths
	print "Do you wish to display closeness centrality of all nodes?\nPress 1 to print"
	deg_dist = input()
	if deg_dist == 1:
		closeness(nodes_closeness)
		print nodes_closeness
	print "\n\n\n"
	print "generating random graph"
	construct_random_graph()
	print randomgraphdict

if __name__ == '__main__':
	main()
