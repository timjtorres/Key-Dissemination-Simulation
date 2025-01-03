import random as rd
import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

# test
# class SecretSharingPrimitive(ig.Graph):
#     def num_vert(self):
#         return self.vcount()

# It would probably be better to add most of these functions as methods to a new class that inherits from ig.Graph
def gen_DAG(NUM_V: int, p: float=0.5):
    """ A simple function for generating a random Directed Acyclic Graph (DAG).

        Paramteres
        ----------
        n : int
            The number of vertices in the graph.
        p : float
            The probability of connecting two vertices (v1, v2) 
            where v2 is of higher topographical order.
        
        Returns
        -------
        G : ig.Graph
            A DAG graph.
    """
    edges = []
    for i in range(NUM_V-1):
        for j in range(NUM_V - i - 1):
            if rd.random() < p:
                edges.append((i, j+i+1))
    G = ig.Graph(NUM_V, edges, directed=True)
    return G

def get_Connect_Sets(G: ig.Graph):
    """Creates a set for each vertex. These sets contain all of the vertices 
        that are connected to a specific vertex. For simplicity, the vertex 
        itself is included in its own set.

        Paramters
        ---------
        G : ig.Graph 
            The graph to be analyzed

        Return
        ------
        Connectivity_sets : list
    """
    NUM_V = G.vcount()
    V_ordered = G.topological_sorting(mode='out')
    Connectivity_sets = [[] for i in range(NUM_V)]
    
    for i in range(NUM_V):
        Connectivity_sets[V_ordered[i]].append(V_ordered[i])
        for j in range(i+1, NUM_V):
            if G.are_adjacent(V_ordered[i], V_ordered[j]):
                for ele in Connectivity_sets[V_ordered[i]]:
                    Connectivity_sets[V_ordered[j]].append(ele)
                Connectivity_sets[V_ordered[j]] = list(set(Connectivity_sets[V_ordered[j]]))
    return Connectivity_sets

def get_Cut_Vertices(G: ig.Graph, source_index: int, target_index: int=None):
    """Find all cut vertices in a DAG graph. Returns a list of these vertices.

        Paramters
        ---------
        G : ig.Graph 
            The graph to be analyzed.
        source_index : int 
            The index of the source in the topologically sorted vertex list.
        target_index : int 
            Topological index of the target

        Returns
        -------
        cut_vertices : list
            A list containing the cut-vertices for a source and target.
            Returns an empty list if vertices are not connected of not cut-vertex exists.
    """
    NUM_V = G.vcount()
    V_ordered = G.topological_sorting(mode='out')
    cut_vertices = []
    source = V_ordered[source_index]
    
    # set source and target
    if target_index == None:
        target = V_ordered[-1]
    else:
        target = V_ordered[target_index]

    # check if source and target are already directly connected
    if G.are_adjacent(source, target):
        print("Source and target are directly connected.\nNo network scheme needed.")
        return cut_vertices
    
    # check if source and desition are connected at all
    if G.vertex_connectivity(source, target, neighbors="ignore") == 0:
        print("Source is not connected to target.")
        print("Invalid graph for algorithm\n")
        return cut_vertices
    
    for i in range(source_index+1, NUM_V-1):
        G_tmp = G.copy()
        G_tmp.delete_vertices(V_ordered[i])
        
        # compensate for graph resizing
        if V_ordered[i] < source:
            source = source - 1
        if V_ordered[i] < target:
            target = target - 1
        
        # if s and d are no longer connected then V_ordered[i] is a cut-vertex, append to list
        if G_tmp.vertex_connectivity(source, target, neighbors="ignore") == 0:
            cut_vertices.append(V_ordered[i])
        
        # reset s and d compensation
        source = V_ordered[source_index]
        target = V_ordered[-1]

    del G_tmp
    return cut_vertices

def intersection(l1: list, l2: list):
    """Returns the intersection of two lists.
    """
    return list(set(l1).intersection(l2))

def Plot_graph(G: ig.Graph, title: str=None, vertex_label: None=None, edge_width: None=0.8, edge_color: None=None, layout: str='kk'):
    """
    Plot the graph and decide which layout to use.
    
    Parameters
    ----------
    G : ig.Graph
        Graph to plot
    layout : str
        The layout to use.
    """
    fig, ax = plt.subplots(figsize=(10,6))
    ig.plot(G,
            layout=layout, 
            target=ax,
            vertex_label_size=10.0,
            vertex_label=vertex_label,
            vertex_size=30,
            edge_width=edge_width,
            edge_color=edge_color,
            edge_arrow_width=5
    )
    plt.suptitle(title)
    plt.show()

def del_cut_edges(G: ig.Graph, cut_vertex: int):
        G_tmp = G.copy()
        in_cut = G.neighbors(cut_vertex, mode='in')
        out_cut = G.neighbors(cut_vertex, mode='out')
        rm_edges_in = [(i, cut_vertex) for i in in_cut]
        rm_edges_out = [(cut_vertex, i) for i in out_cut]
        rm_edges = rm_edges_in + rm_edges_out
        G_tmp.delete_edges(rm_edges)
        return G_tmp

def get_intersectionSet_hEdges(Connectivity_sets: list, in_cut_d: list, NUM_V):
    # Check for intersection bewtween vertex sets, also add edges between sets that intersect
    edges_H = []
    Intersection_sets = [[] for i in range(NUM_V)]
    for i in in_cut_d:
        for j in in_cut_d:
            intersect = intersection(Connectivity_sets[i], Connectivity_sets[j])
            if len(intersect) > 0 and (i != j):
                if (in_cut_d.index(j), in_cut_d.index(i)) in edges_H:
                    continue
                else:
                    edges_H.append((in_cut_d.index(i), in_cut_d.index(j)))
                
                d = (j, intersect)
                Intersection_sets[i].append(d)
   
    return Intersection_sets, edges_H

def Func_1(G: ig.Graph, source: int, target: int):
    """
    For each cut vertex determine if an alternating paths exists.

    Parameters
    ----------
    G : ig.Graph
        Graph being analyzed
    source : int
        The source vertex
    target : int
        The target vertex
    
    Returns
    -------
    P_alt_exists : list
        List of tuples of the form (cut-vertex, bool). If alternating path does not exist for a cut-vertex, cv, then tuple 
        entry is (cv, False), otherwise entry is (cv, True)

    """
    # Find the cut vertices and place them in a list
    NUM_V = G.vcount()
    V_sort = G.topological_sorting(mode="out")
    cut_vertices = get_Cut_Vertices(G, V_sort.index(source))

    P_alt_exists = []

    # remove all edges connected to the cut vertex (assuming only 1 cut vertex)
    for vert in cut_vertices:
        G_tmp = del_cut_edges(G, vert)
        
        # add the target to list containing vertices in-coming to the cut vertex
        in_cut_d = G.neighbors(vert, mode='in')
        in_cut_d.append(target)
        
        Connectivity_sets = get_Connect_Sets(G_tmp)
        Intersection_sets = [[] for i in range(NUM_V)]
        edges_H = []
        
        # Check for intersection bewtween vertex sets, also add edges between sets that intersect
        Intersection_sets, edges_H = get_intersectionSet_hEdges(Connectivity_sets, in_cut_d, NUM_V)

        # Now that we have intersection sets, make a meta graph H and find a path
        # By design, first element in H is the source and last element in H is the target
        num_vertices_H = len(in_cut_d)
        H = ig.Graph(num_vertices_H, edges_H, directed=False)

        # Get a shortest path in the graph H.
        P_alt_H = H.get_shortest_paths(source, in_cut_d.index(target))[0]
        if len(P_alt_H) == 0:
            P_alt_exists.append(vert, False)
        else:
            P_alt_exists.append((vert, True))

    return P_alt_exists

def Analyze_graph(G: ig.Graph, source: int=None, target: int=None, debug: bool=False):
    """ 
    Analyze the graph and return the alternating path, if there is one.
        
    Parameters
    ----------
    G : ig.Graph
        The graph to analyze.
    source : int
        The index of the source vertex in the graph G.
    target : int
        The index of the target vertex in the graph G.
    debug : bool
        Provide information about graph analysis to verify things are working correctly.
        Prints 
            - Graph G
            - Cut_vertices
            - Vertices incoming to cut-vertex
            - Connection sets
            - Intersection sets
            - Path taken from meta-graph H
    
    Returns 
    -------
    Paths : dict()
        - Path from source to target
        - Alternating path
    """
    NUM_V = G.vcount()
    V_ordered = G.topological_sorting(mode='out') # Place the vertices in topoligocal order
    
    # setting up the target and source if not set
    if target == None:
        target = V_ordered[-1] # For now, set the target to the last topoligically ordered 
    if source == None:
        source = 0
        source_index = V_ordered.index(source)
    
    # Find the cut vertices and place them in a list
    cut_vertices = get_Cut_Vertices(G, source_index)

    # remove all edges connected to the cut vertex (assuming only 1 cut vertex)
    G_tmp = G.copy()
    in_cut = G.neighbors(cut_vertices[0], mode='in')
    out_cut = G.neighbors(cut_vertices[0], mode='out')
    rm_edges_in = [(i, cut_vertices[0]) for i in in_cut]
    rm_edges_out = [(cut_vertices[0], i) for i in out_cut]
    rm_edges = rm_edges_in + rm_edges_out
    G_tmp.delete_edges(rm_edges)
    
    # add the target to list containing vertices in-coming to the cut vertex
    in_cut_d = in_cut.copy()
    in_cut_d.append(target)

    Connectivity_sets = get_Connect_Sets(G_tmp)
    Intersection_sets = [[] for i in range(NUM_V)]
    edges_H = []

    # Check for intersection bewtween vertex sets, also add edges between sets that intersect
    for i in in_cut_d:
        for j in in_cut_d:
            intersect = intersection(Connectivity_sets[i], Connectivity_sets[j])
            if len(intersect) > 0 and (i != j):
                # if V_ordered.index(i) < V_ordered.index(j): # topologial order may not remain
                if (in_cut_d.index(j), in_cut_d.index(i)) in edges_H:
                    continue
                else:
                    edges_H.append((in_cut_d.index(i), in_cut_d.index(j)))
                d = (j, intersect)
                Intersection_sets[i].append(d)

    # Now that we have intersection sets, make a meta graph H and find a path
    # By design, first element in H is the source and last element in H is the target
    num_vertices_H = len(in_cut_d)
    H = ig.Graph(num_vertices_H, edges_H, directed=False)
    H.vs["name"] = np.arange(0, num_vertices_H)
    H.vs[0]["name"] = 'S'
    H.vs[-1]["name"] = 'D'

    # Get a shortest path in the graph H.
    P_alt_H = H.get_shortest_paths(source, in_cut_d.index(target))[0]
    if len(P_alt_H) == 0:
        print("No alternating path exists.\n")

    # Get the alternating path
    P_alt = []
    for i in range( 1, len(P_alt_H) ):
        P_alt_H_to_G_prev = in_cut_d[P_alt_H[i-1]]
        P_alt_H_to_G = in_cut_d[P_alt_H[i]]
        inter_tmp = Intersection_sets[P_alt_H_to_G_prev] # select the intersection set for vertex P_alt_H[i-1]
        for j in range( len(inter_tmp) ):
            i_set_tuple = inter_tmp[j]          # choose the jth tuple in the intersection set
            if i_set_tuple[0] == P_alt_H_to_G:    # check if the first element of the tuple (the vertex set) is equal to the next vertex in the alternating path
                if P_alt_H_to_G_prev != source or len(P_alt_H) == 2:   # just to account for the first step (starting at the source)
                    P_alt.append(G_tmp.get_shortest_paths(i_set_tuple[1][0], P_alt_H_to_G_prev)[0]) # append the shortest path from an intersecting vertex to the current collider
                P_alt.append(G_tmp.get_shortest_paths(i_set_tuple[1][0], P_alt_H_to_G)[0])    # append the shortest path from an intersecting vertex to the next collider

    source_to_target = G.get_shortest_paths(source, target)[0]
    Paths = {"Alternating path": P_alt, "Source to target": source_to_target}

    # Print some debug info
    if debug == True:
        print(f"{G}\n")
        print(f"Cut-vertices: {cut_vertices}\n")
        print(f"Incoming to cut-vertex: {in_cut}\n")
        for i in range(NUM_V):
            print(f"Connect set {i}: {Connectivity_sets[i]}")
        print("\n")
        for i in range(NUM_V):
            print(f"Intersection set {i}: {Intersection_sets[i]}")
        print("\n")
        print(f"Graph-H Path: {P_alt_H}\n")

    print(f"Alternating path: {Paths['Alternating path']}\n")
    print(f"Path to target: {Paths['Source to target']}\n")

    # Just for aesthetics
    # Want to make edges in alternating path bolded
    alt_edges = []
    for i in range(len(P_alt)):
        for j in range(len(P_alt[i]) - 1):
            alt_edges.append((P_alt[i][j], P_alt[i][j+1]))
    alt_edge_ids = G.get_eids(alt_edges)
    edge_widths = [3 if i in alt_edge_ids else 1 for i in range(G.ecount())]
    edge_colors = ["#000000" if i in alt_edge_ids else "#555555" for i in range(G.ecount())]

    # Plot the graphs
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6,6))
    ax1.set_title("Graph G")
    ax2.set_title("Graph H")
    ig.plot(G,
            layout='kk', 
            target=ax1,
            vertex_label_size=10.0,
            vertex_label=[i for i in range(NUM_V)],
            vertex_size=30,
            edge_width=edge_widths,
            edge_color=edge_colors,
            edge_arrow_width=5
    )
    ig.plot(H,
            layout='kk', 
            target=ax2,
            vertex_label_size=10.0,
            vertex_label=H.vs["name"],
            vertex_size=30,
            edge_width=1,
            edge_arrow_width=5
    )
    plt.show()

    return Paths