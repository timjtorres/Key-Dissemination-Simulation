import numpy as np
import random as rd
import matplotlib.pyplot as plt
import igraph as ig
from network_algs import *

def Gen_graph():
    NUM_V_I = 5
    NUM_V_II = 5
    NUM_V_III = 1
    NUM_V_IV = 15
    NUM_V = NUM_V_I + NUM_V_II + NUM_V_III + NUM_V_IV

    I_I = np.transpose( np.tri(NUM_V_I, k=-1, dtype=int) )
    I_II = np.zeros((NUM_V_I, NUM_V_II), int)
    I_III = np.transpose( np.asmatrix([1, 0, 0, 1, 1], dtype=int) )
    I_IV = np.zeros((NUM_V_I, NUM_V_IV), int)

    II_I = np.zeros((NUM_V_II, NUM_V_I), int)
    II_II = np.transpose( np.tri(NUM_V_II, k=-1, dtype=int) )
    II_III = np.zeros((NUM_V_II, NUM_V_III), int)
    II_IV = np.zeros((NUM_V_II, NUM_V_IV), int)

    III_I = np.zeros((NUM_V_III, NUM_V_I), int)
    III_II = np.asmatrix([1, 0, 1, 1, 1], dtype=int)
    III_III = np.asmatrix([0])
    III_IV = np.zeros((NUM_V_III, NUM_V_IV), int)

    IV_I = np.tri(NUM_V_IV, NUM_V_I, k=-1, dtype=int)
    IV_II = np.tri(NUM_V_IV, NUM_V_II, k=-1, dtype=int)
    IV_III = np.transpose( np.asmatrix([1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]) )
    IV_IV = np.transpose( np.tri(NUM_V_IV, k=-1, dtype=int) )

    Adj = np.block([[I_I, I_II, I_III, I_IV],
                    [II_I, II_II, II_III, II_IV],
                    [III_I, III_II, III_III, III_IV],
                    [IV_I, IV_II, IV_III, IV_IV]
                    ])

    G = ig.Graph.Adjacency(Adj, mode="directed")
    return G

if __name__ == "__main__": 
    
    G = Gen_graph()
    NUM_V = G.vcount()
    s = 0
    t = G.topological_sorting(mode='out')[-1]
    S = ShareSecret(G, s, t)
    P_alt, H = S.get_alternating_path(Graph_H=True)
    # print(S.connectivity_sets)
    # print(S.intersection_sets)
    print(P_alt)

    # Put alternating path edges in bold 
    alt_edges = []
    for i in range(len(P_alt)):
        for j in range(len(P_alt[i]) - 1):
            alt_edges.append((P_alt[i][j], P_alt[i][j+1]))
    alt_edge_ids = G.get_eids(alt_edges)
    edge_widths = [3 if i in alt_edge_ids else 1 for i in range(G.ecount())]
    edge_colors = ["#000000" if i in alt_edge_ids else "#555555" for i in range(G.ecount())]

    # Plot graph G and H
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