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
    s = 0
    t = G.topological_sorting(mode='out')[-1]
    S = ShareSecret(G, s, t)
    P_alt = S.get_alternating_path()
    print(S.connectivity_sets)
    print(S.intersection_sets)
    print(P_alt)