import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
from network_algs import *

# Test with inheritance
# class Child(ig.Graph):
#     def __init__(self, n=0, edges=None, directed=False, targets=None):
#         self.targets = targets
#         super().__init__(n, edges, directed)
#         print(self.topological_sorting(mode='out'))

    

if __name__ == "__main__":
    NUM_V = 8
    s1, s2, u1, u2, w1, w2, d1, d2 = 0, 1, 2, 3, 4, 5, 6, 7
    V_label = ["s1", "s2", "u1", "u2", "w1", "w2", "d1", "d2"]
    EDGES = [(s1, u1), (s1, d2), (s2, u2), (s2, d1), (u1, d1), (u2, d2), (w1, s1), (w1, d1), (w2, s2), (w2, d2)]
    # K = Child([6, 7], NUM_V, EDGES, True)
    G = ig.Graph(n=NUM_V, edges=EDGES, directed=True)
    K = ShareKey(G, targets=[6,7])
   
    print(K.does_scheme_exist())

    fig, ax = plt.subplots()
    ig.plot(G, 
        target=ax,
        vertex_label=V_label
    )
    plt.show()