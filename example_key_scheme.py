import matplotlib.pyplot as plt
from network_algs import *


def main():

        ###################################
        # Network 1: Should return True
        ###################################
        NUM_V = 8
        s1, s2, u1, u2, w1, w2, d1, d2 = 0, 1, 2, 3, 4, 5, 6, 7
        V_label1 = ["s1", "s2", "u1", "u2", "w1", "w2", "d1", "d2"]
        EDGES = [(s1, u1), (s1, d2), (s2, u2), (s2, d1), (u1, d1), (u2, d2), (w1, s1), (w1, d1), (w2, s2), (w2, d2)]
        G1 = ig.Graph(NUM_V, EDGES, directed=True)

        K1 = ShareKey(G1, [6,7])
        print(f"Scheme exists for network 1: {K1.does_scheme_exist()}\n")


        ###################################
        # Network 2: Should return False
        ###################################
        NUM_V = 7
        s1, s2, u, w1, w2, d1, d2 = 0, 1, 2, 3, 4, 5, 6
        V_label2 = ["s1", "s2", "u1", "u2", "w1", "w2", "d1", "d2"]
        EDGES = [(s1, u), (s2, u), (u, d1), (u, d2), (w1, s1), (w1, d1), (w2, s2), (w2, d2)]
        G2 = ig.Graph(NUM_V, EDGES, directed=True)

        K2 = ShareKey(G2, [5, 6])
        print(f"Scheme exists for network 2: {K2.does_scheme_exist()}\n")

        # Plot the networks
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.set_title("Network 1")
        ax2.set_title("Network 2")

        ig.plot(G1, target=ax1, vertex_label=V_label1)
        ig.plot(G2, target=ax2, vertex_label=V_label2)
        plt.show()
        

if __name__ == "__main__":
        main()