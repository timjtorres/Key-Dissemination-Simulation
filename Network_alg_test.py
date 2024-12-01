import numpy as np
import random as rd
import matplotlib.pyplot as plt
import igraph as ig
from network_algs import *


if __name__ == "__main__": 
    
    plot = True
    NUM_V = 30

    # Generate a random DAG
    G = ig.Graph.Erdos_Renyi(n=NUM_V, m=70, directed=False, loops=False)
    G.to_directed(mode='acyclic')
    print(G)

    # Order the vertices topologically    
    V_ordered = G.topological_sorting(mode='out')
    print(f"\nTopographical order: {V_ordered}\n")

    # Define the destination in the network as the last topographical vertex
    destination = V_ordered[NUM_V-1]

    ##########################################################
    # ***Determine which vertex will be the source***
    ##########################################################
    # Want to randomly choose a valid source. 
    # To be valid must have outgoing edges and not too close to the dest (topologically)
    # Not a good way of doing it, but works for now, should find min # of nodes needed to implement alg
    source_index = rd.randint(0, NUM_V // 2)
    source = V_ordered[source_index]
    print(f"Source: {source}\n")

    # Do a very basic check to see if s and d are neighbors, if they are, we're done
    if G.are_adjacent(source, destination) == 1:
        print("\nSource and destination are neighbors.\nPath: s -> d")
    else:
        cut_vertices = get_Cut_Vertices(G, source_index)
        print(f"***Cut vertices: {cut_vertices}***\n")
        
        Connectivity_sets = get_Connect_Sets(G)
        
        # incoming edges to cut vertex
        print(f"AdjList: {G.get_adjlist(mode='in')}\n")

        for i in range(NUM_V):
            print(f"Vertex {i} Set: {Connectivity_sets[i]}")

    if plot == True:
        fig, ax = plt.subplots(figsize=(10,6))
        ig.plot(G,
                layout='grid', 
                target=ax,
                vertex_label_size=6.0,
                vertex_label=range(NUM_V),
                vertex_size=30,
                edge_width=0.8,
                edge_arrow_width=5
        )
        plt.show()