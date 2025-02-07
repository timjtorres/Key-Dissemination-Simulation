import numpy as np

from network_algs import *


def main():
        
        NUM_V = 8
        s1, s2, u1, u2, w1, w2, d1, d2 = 0, 1, 2, 3, 4, 5, 6, 7
        V_label = ["s1", "s2", "u1", "u2", "w1", "w2", "d1", "d2"]
        EDGES = [(s1, u1), (s1, d2), (s2, u2), (s2, d1), (u1, d1), (u2, d2), (w1, s1), (w1, d1), (w2, s2), (w2, d2)]
        G1 = ig.Graph(NUM_V, EDGES, directed=True)
        G2 = ig.Graph(NUM_V, EDGES, directed=True)

        G1_U_G2= ig.disjoint_union([G1, G2])
        print(G1_U_G2)

        fig, ax = plt.subplots()
        ig.plot(G1_U_G2, 
                target=ax
        )
        plt.show()


        # NUM_V = 7
        # s1, s2, u, w1, w2, d1, d2 = 0, 1, 2, 3, 4, 5, 6
        # V_label = ["s1", "s2", "u1", "u2", "w1", "w2", "d1", "d2"]
        # EDGES = [(s1, u), (s2, u), (u, d1), (u, d2), (w1, s1), (w1, d1), (w2, s2), (w2, d2)]
        # G = ig.Graph(NUM_V, EDGES, directed=True)
        
        # fig, ax = plt.subplots()
        # ig.plot(G, 
        #         target=ax,
        #         vertex_label=range(NUM_V)
        # )
        # plt.show()

        # D = []
        # print(F2(G, D))
        # print(G.topological_sorting(mode='out'))

        # fig, ax = plt.subplots()
        # ig.plot(G, 
        #         target=ax,
        #         vertex_label=range(NUM_V)
        # )
        # plt.show()


if __name__ == "__main__":
        main()

# NUM_V = 50
# NUM_OUT = 3 

# G = ig.Graph().Barabasi(NUM_V, NUM_OUT, directed=True)
# print(G.is_dag())


# cut_vertices = get_Cut_Vertices(G, 0, 19)
# print(f"Topological order: {G.topological_sorting(mode='out')}")
# print(f"cut-vertices: {cut_vertices}")

# fig, ax = plt.subplots(1, 1, figsize=(6,6))
# ig.plot(G, 
#         target=ax,
#         layout='kk',
#         vertex_label = range(NUM_V),
#         vertex_label_size = 8,
#         edge_arrow_width=5,
#         edge_width=1)
# plt.show()