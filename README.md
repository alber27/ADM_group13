## Algorithmic Methods of Data Mining   

# Homework 4  

### Group 13 :  

##### Alberto Piva  1757137  

##### Giorgia Vicari  1656899  

##### Temirlan Zharkynbek  1793815  



### Exercise 1  

The purpose of this exercise is to create a graph from *reduced_dblp.json*, build a suitable procedure on it, and then make it run with another file, *full_dblp.json*.  

The initial file is structured as a list of dictionaries. Every dictionary contains informations about a specific conference:   

`authors`  

`id_conference`  

`id_conference_int`  

`id_publication`  

`id_publication_int`  

`title`  

Inside authors there is another list of dictionaries and each of them contains informations about every single author that partecipated at the conference:  

`author`  

`author_id`  

The building of the graph is based on creating an edge between two authors only if they have been in the same conference, then weight the edge using Jaccard similarity.  

Every passage regarding the building of the graph is done using networkx functions.  

The procedure we use starts creating one node for every single `author_id` found in the initial file, and adding `author` as attribute of the node.  

While building edges, the first thing to check is if there was only one author in the conference. If true, we have no possibility to create edges with only one node. Otherwise, the authors are stored in a temporary list and sorted in order to avoid the creation of mutual edges (e.g. a-b and b-a) given that we are in an undirected graph, and probably several issues while weighting the graph. If an edge between two nodes is created we assign it a weight of 1, while if we find an already existing edge, a value of 1 is added to the current weight.  

At the end the weight of the edges is modified basing on Jaccard similarity.  

More info about this exercise in the subsections `def graph_nodes` and `def graph_edges` of **modules_group13.py** .  


### Exercise 2.a  

*Given a conference in input, return the subgraph induced by the set of authors who published at the input conference at least once. Once you have the graph, compute some centralities measures (degree, closeness, betweeness) and plot them.*

The exercise is solved by taking all the nodes that are in the given conference and store all of them into a list.   

The list is passed to the networkx function `subgraph` that creates a subgraph of the given nodes, starting from the base graph G. It's computed as follows:   

`G.subgraph(list_of_nodes)`  

To compute the centralities measures (degree-closeness-betweeness), the homonyms functions of networkx are used:    

`nx.degree_centrality( )`  
`nx.betweenness_centrality( )`    
`nx.closeness_centrality( )`  

The plots consist in the whole subgraph of the conference, where the nodes are coloured with gradations of more intense color if they have a higher value of the respective centrality measure.     

More info about this exercise in the subsections `def get_conference_ids`, `def conference_authors` and `def plot_centrality` of **modules_group13.py** .    


### Exercise 2.b  

*Given in input an author and an integer d, get the subgraph induced by the nodes that have hop distance (i.e., number of edges) at most equal to d with the input author. Then, visualize the graph.*  

To return the subgraph of the nodes that have a maximum hop distance from the given author node, we need to search the neighbors of the first node and append them in a list. Iteratively, for a range of *d* iterations, we search for the neighbors of the nodes inside the list.  

Also this list is passed to the networkx function `subgraph` to create a subgraph of the given nodes, starting from the base graph G. The resulting graph is then plotted.  

More info about this exercise in the subsection `def d_hops` of **modules_group13.py** .   





### modules_group13.py  

##### `def graph_nodes(builder)`    

This function takes in input *reduced_dblp.json* or *full_dblp.json*, searches inside the given file for all the `author_id` to create the nodes of the graph and adds as attribute of the node the proper `author` (name of the author).  

In the meantime, it also creates a dictionary with `author_id` as key and the total number of appearances in all the conferences as attribute. This dictionary will be used to compute the Jaccard similarity.  

The function returns the graph and the dictionary.  


##### `def graph_edges(graph, builder, author_dict)`    

The function takes in input:  
- the graph without edges   
- *reduced_dblp.json* or *full_dblp.json*   
- a dictionary with `author_id` as key and the total number of appearance in all the conferences as attribute.  

It creates edges between nodes if their `author_id` appear at the same conference in the builder file, and gives to the edge a weight of 1. If the same nodes as before are in another conference, a weight of 1 is added to the edge.  

Finally it computes the Jaccard similarity on the edges using the proper definition: 1 - (intersection(*a*, *b*) / union(*a*, *b*)), where *a* and *b* are nodes, the intersection between them is the current weight of the edge, and the union is the sum of the key values of the dictionary (without their intersection), where *a* and *b* are the keys.  

In conclusion the function returns the graph with the weighted edges.

##### `def get_conference_ids(builder)`

The function takes in input *reduced_dblp.json* or *full_dblp.json*

It searches for all the identifiers of the conferences inside the given file and returns a list of uniques identifiers. We use it to check if the conf_ID given in input exists.

##### `def conference_authors(builder, graph, conference_id)`    

The function takes in input *reduced_dblp.json* or *full_dblp.json*, a graph, and the id number of a conference.

It searches inside the builder for all the nodes that are in the conference of the given id and store them in a list. A set is computed for that list.  

Once the set is created, it is passed to the networkx function `subgraph` , that works as follows:  

`graph.subgraph(set_auth)`, where *set_auth* is the set of nodes (re-tranformed in list).  

The resulting subgraph is returned.  


##### `def plot_centrality(c_dict, subgraph, title)`    

This function takes in input:  
- a dictionary with the `author_id` as key and the value of a centrality measure as attribute  
- a subgraph  
- a string if i want to give a title to the plot.  

The function creates a dataframe with two columns: `node` and `values` . It uses them to assign the names to the nodes and to color a node with gradations of more intense color of red if its degree is higher than the other nodes, using the networkx function:   

`nx.draw(subgraph, with_labels = True, node_color = df['values'], cmap = plt.cm.Reds)`  

The plot is then showed and saved.  


##### `def d_hops(d, node, graph)`  

This function takes in input an integer *d*, a node identified with a valid `author_id`, and a graph.  

It computes and inserts in a list the neighbors of the given node. Therefore, for a number equal to *d* of times, it searches for the neighbors of the nodes inside the list and keep inserting the results.  

After *d* iterations it removes the duplicates and pass the resulting list to the networkx function `graph.subgraph(seen_nodes)`, where *seen_nodes* is the resulting list and plot the final subgraph using`nx.draw(K)`, where *K* is the subgraph.  


##### `def shortest_path(G, source, target)`

The function takes in input a graph, and two nodes identified with a valid `author_id` as *source* and *target*.   
It creates two dictionaries: one for path computing called `pred`, initialized with all the existing `author_id` (nodes) as keys and the same `author_id` as attibute, and the other one called `dist` for distance computing, initialized with all the `author_id` as keys and a starting distance equal to an infinite number.  
The source node distance is then setted to 0. Using the heap queue algorithm, the starting node and its distance are inserted in the `queue` list.  

Until the node is not found and `queue` is not empty the function keep taking from `queue` the first element using the heap queue algorithm, that contains the node and its distance as explained above. Using the node, it searches for all the nieghbors and takes the weight of the edge and check if the retrieved weight, intended as distance, is lower than the one that is stored in `dist`. If it is lower, it substitutes the current value of the current node in `dist` with the new minimum distance, and substitutes the current value of the current node in `pred` with the proper predecessor node.  

If it isn't possible to find a path between *source* and *target*, it returns a NAn value.  
Else, if there is a possible path, it searches for all the info stored in `path` and `dist` to return the minimum distance and the path with all the intermediate node that are in the minumun path to reach the target node from the source node.  


##### `def group_number(node_list, graph)`

The function takes in input a list of nodes with a valid `author_id` and a graph.  

It creates a dictionary with all the `author_id` of the given list of nodes as keys.  

For each key of the dictionary it uses the previous function, `def shortest_path`, to compute the minimum path for every node of the graph. If no path is found it pass, otherwise if for one or more key of the dictionary a path that connect to a node exists, the current node is stored as attribute of the key with the shortest path.  

In the end it's returned the dictionary with the same keys as before and as attributes the nodes the have the shortest path with the proper key.