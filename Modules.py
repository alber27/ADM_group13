import networkx as nx
import matplotlib.pyplot as plt
import heapq
import numpy as np
from collections import defaultdict
import pandas as pd


############################################################
############################################################
############################################################


def graph_nodes(builder):

    auth_publ = {}
    auth_ = []

    G = nx.Graph()
    
    for i in builder:
        for a in i['authors']:
            # for every author of a conference we create a node
            # and also we store in a dictionary how many publications this author have done
            try:
                auth_publ[a['author_id']] += 1
            except KeyError:
                G.add_node(a['author_id'])
                #G[builder[i]['authors'][a]['author_id']]['author'] = builder[i]['authors'][a]['author']
				#the line above is to assign the name of authors to each node
                auth_publ[a['author_id']] = 1
                auth_.append(a['author_id'])

    return G, auth_publ
    

############################################################
############################################################
############################################################

    
def graph_edges(graph, builder, author_dict):
    
    for i in builder:
    # if only one author was in a publication we have no edges
        if len(i['authors']) > 1:
            edge_list = []
            for j in i['authors']:
                edge_list.append(j['author_id'])
            # need to create a list to store all authors of the same publications, because it may happen that 
            # we have (a, b) and (b, a) and they are different! So we want to store all IDs in a sorted list.
            edge_list.sort()
            for a in range(len(edge_list)):
                for b in range(a + 1,len(edge_list)):
                    try:
                        graph[edge_list[a]][edge_list[b]]['weight'] += 1
                    except KeyError:
                        graph.add_edge(edge_list[a], edge_list[b], weight = 1)

    # here we are going to assign the weight of edges basing on Jaccard similarity
    for a, b in graph.edges():
        if b != 'author' and a != 'author':
            graph[a][b]['weight'] = 1 - (graph[a][b]['weight'] / (author_dict[a] + author_dict[b] - graph[a][b]['weight']))

    return graph

############################################################
############################################################
############################################################    
    
def get_conference_ids(builder):    
    conference_ids = set()
    for i in builder:
        conference_ids.add(i['id_conference_int'])
    
    return conference_ids
	
############################################################
############################################################
############################################################

def conference_authors(builder, graph, conference_id):
    
    set_auth = set()
    
    # for a specific conference we store all the authors that took part at least once to that conference
    for i in builder:
        if i['id_conference_int'] == conference_id:
            for j in i['authors']:
                set_auth.add(j['author_id'])
    
    # once we have all the authors, we take the subgraph with just the author's nodes
    set_auth = list(set_auth)
    set_auth.sort()
    subgraph = graph.subgraph(set_auth)
    
    return subgraph


############################################################
############################################################
############################################################


def plot_centrality(c_dict, subgraph, title):
    df = pd.DataFrame()
    df['node'] = c_dict.keys()
    df['values'] = c_dict.values()
    nx.draw(subgraph, with_labels = True, node_color = df['values'], cmap = plt.cm.Reds)
    plt.savefig(str(title) + '.png')

############################################################
############################################################
############################################################


def d_hops(d, node, graph):
    
    seen_nodes = []
    new_hop = []
    
    seen_nodes.append(node)
    
    # at each step we find the neighbors of the stored nodes
    for i in range(d):
        for n in seen_nodes:
            for next_h in nx.neighbors(graph, n):
                if next_h != 'author':
                    new_hop.append(next_h)
    
        for root in new_hop:
            seen_nodes.append(root)
        
        new_hop = []
    
    # we pass the list of nodes to the nx.subgraph functions to have the graph of the nodes we want
    seen_nodes = list(set(seen_nodes))
    seen_nodes.sort()
    K = graph.subgraph(seen_nodes)
    
    nx.draw(K)
    plt.show()
    plt.savefig('hops.png')
    
    
############################################################
############################################################
############################################################


def shortest_path(G, source, target):
    inf = np.inf
    # creates two dictionaries, one for path and one for distances between nodes
    pred = { x:x for x in G }
    dist = { x:inf for x in G }
    # sets distance of source-source to 0
    dist[source] = 0
    queue = []
    # pushes distance from source (0) and source to queue
    heapq.heappush(queue, [dist[source], source])
 
    while(queue):
        # returns the smallest item from queue
        u = heapq.heappop(queue)
        u_dist = u[0]
        u_id = u[1]
        if u_dist == dist[u_id]:
            # for each node in the neighbors we take the weight of the edge
            for node in G[u_id]:
                if node != 'author':
                    node_id = node
                    node_w = G[u_id][node]['weight']

                # check if the new distance is lower than the one that is stored in dist{}, if it is, we substitute
                # also push into queue the values of the node and update pred{}
                if dist[u_id] +  node_w < dist[node_id]:
                    dist[node_id] = dist[u_id] + node_w
                    heapq.heappush(queue, [dist[node_id], node_id])
                    pred[node_id] = u_id

    # got no path :(            
    if dist[target] == inf:
        return np.nan, np.nan
        
    # retrieve informations from dict to return results
    else:
        st = []
        node = target
        
        while(True):
            st.append(str(node))
            if(node == pred[node]):
                break
            
            node = pred[node]
        path = st[::-1]
        
    return dist[target], path


############################################################
############################################################
############################################################

def group_number(node_list, graph):
    
    group_dict = defaultdict(list)
    # new key for every node in the node list    
    for node in node_list:
        group_dict[node]

    # for every key we compute the minimum path for each node, sort by distance and assign each node to its group if distance is not nan
    for curr_n in graph.nodes():
        dst = np.inf
        p = 0
        min_path = []
        for root in node_list:
            try:
                dst, p = shortest_path(graph, root, curr_n)
            except:
                TypeError
                
            if dst is not np.nan:
                min_path.append([dst, root])
                min_path.sort(key=lambda x: x[0])
            
        if min_path:
            group_dict[min_path[0][1]].append(curr_n)
            
    return group_dict        
	