import json
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import numpy as np
from collections import defaultdict
import pandas as pd
import Modules as fn

full = json.load(open('full_dblp.json','r'))
reduced = json.load(open('reduced_dblp.json','r'))

#############
## POINT 1 ##
#############

G, auth_publ = fn.graph_nodes(full)
G = fn.graph_edges(G, full, auth_publ)


#############
## POINT 2 ##
#############

'''2.a) given a conference in input, return the subgraph induced by the set of authors who
published at the input conference at least once. Once you have the graph, compute
some centralities measures (degree, closeness, betweeness) and plot them.'''


conf_IDs = fn.get_conference_ids(full)

#conf_id = input()
conf_id = 4634

if conf_id not in conf_IDs:
    print('Please choose a valid conference ID')
    print()
    print('Please select a valid conference ID between the followings: ')
    print(conf_IDs)
else:    
    H = fn.conference_authors(full, G, conf_id)


deg_c = nx.degree_centrality(H)
bet_c = nx.betweenness_centrality(H)
clo_c = nx.closeness_centrality(H)

fn.plot_centrality(deg_c, H, 'degree')
fn.plot_centrality(bet_c, H, 'betweeness')
fn.plot_centrality(clo_c, H, 'closeness')

'''2.b) given in input an author and an integer d, get the subgraph induced by the nodes that
have hop distance (i.e., number of edges) at most equal to d with the input author.
Then, visualize the graph.'''

#d = int(input())
d = 2
#node = input()
node = 48715

if node not in G.nodes():
    print('Please choose a valid node for node')
    print()
else:
	fn.d_hops(d, node, G)


#############
## POINT 3 ##
#############

'''3.a) Write a Python software that takes in input an author (id) and returns the weight of the
shortest path that connects the input author with Aris. Here, as a measure of distance
you use the weight w(a1,a2) defined previously.'''

#for node in G.nodes():
#    if G[node]['author'] == 'aris anagnostopoulos':
#        print(node) 
# Aris node = 256176 

#source = input()
source = 16617
target = 256176 # Aris node

if source not in G.nodes():
    print('Please choose a valid node for source')
    print()
if target not in G.nodes():
    print('Please choose a valid node for target')
    print()
else:    
    dist, path = fn.shortest_path(G, source, target)


if dist is np.nan:
    print('There is no path aviable to reach the node ' + str(G[target]['author']) + ' from the node ' + str(G[source]['author']))
else:
    print('The minimum weighted path is: ' + str(dist))
    print('The path to reach the target is: ' + ' -> '.join(path))
    
    
'''3.b) Write a Python software that takes in input a subset of nodes (cardinality smaller than 21) and returns, 
for each node of the graph, its GroupNumber, defined as follow: GroupNumber(v) = min{ShortestPath(v,u)},
where v is a node in the graph and I is the set of input nodes.'''

#node_list = input().split()
node_list = [143709, 205236, 2067]

g_dict = fn.group_number(node_list, G)

for group in g_dict.keys():
    print('NODES IN GROUP NUMBER: ' + str(group))
    print(g_dict[group])
    print('------------------------------------')
