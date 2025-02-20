import matplotlib.pyplot as plt
import igraph as ig

from network_algs import ShareSecret
    
################################
# Find alt path for network G
################################
NUM_V = 12
s, u, t = 0, 1, 10
y, x= [2, 3, 4, 5], [6, 7, 8, 9]
v = 11
EDGES = [(s, u), (s, y[0]), (y[0], u), (y[1], u), (y[2], u), (y[3], u), 
    (x[0], y[0]), (x[0], y[1]), (x[1], y[1]), (x[1], y[2]), (x[2],y[2]), 
    (x[2], y[3]), (x[3], y[3]), (x[3], v), (u, t), (v, t)]
G = ig.Graph(NUM_V, EDGES, directed=True)   # create network
G.vs["name"] = ["s", "u","$y_1$", "$y_2$", "$y_3$", 
               "$y_4$", "$x_1$", "$x_2$", "$x_3$", "$x_4$", "t", "*"]

S = ShareSecret.ShareSecret(G, s, t)    # Initialize SecretShare class with network, source and target
Path, H = S.get_alternating_path(Graph_H=True)  # Get the alternating path (and graph H for plotting)


################################
# Visualize the graphs
################################

# Put alternating path edges in bold 
alt_edges = []
for i in range(len(Path)):
    for j in range(len(Path[i]) - 1):
        alt_edges.append((Path[i][j], Path[i][j+1]))
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