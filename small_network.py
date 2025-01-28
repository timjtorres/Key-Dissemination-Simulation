import numpy as np
import random as rd
import matplotlib.pyplot as plt
import igraph as ig
from network_algs import *

if __name__ == "__main__": 
    
    # The number of vertices
     NUM_V = 12

     s, u, d = 0, 1, 10
     y, x= [2, 3, 4, 5], [6, 7, 8, 9]
     v = 11
     edges = [(s, u), (s, y[0]), (y[0], u), (y[1], u), (y[2], u), (y[3], u), 
         (x[0], y[0]), (x[0], y[1]), (x[1], y[1]), (x[1], y[2]), (x[2],y[2]), 
         (x[2], y[3]), (x[3], y[3]), (x[3], v), (u, d), (v, d)]

     # Make the graph
     G = ig.Graph(NUM_V, edges, directed=True)
     G.es["capacity"] = [1 for i in range(NUM_V)]
     G.vs["name"] = ["s", "u","$y_1$", "$y_2$", "$y_3$", 
                    "$y_4$", "$x_1$", "$x_2$", "$x_3$", "$x_4$", "d", "*"]
    

    #  print(f"{G.topological_sorting(mode='out')}")
     print(F1(G, s, d, u))
     P = Analyze_graph(G, debug=False)
     # print(P)