import igraph as ig
import matplotlib.pyplot as plt
import numpy as np

# Test with inheritance
# class Child(ig.Graph):
#     def __init__(self, n=0, edges=None, directed=False, targets=None):
#         self.targets = targets
#         super().__init__(n, edges, directed)
#         print(self.topological_sorting(mode='out'))

class ShareKey:

    def __init__(self, Graph: ig.Graph, targets = None):
        self.Graph = Graph
        self.targets = targets
        self.topological_order = Graph.topological_sorting(mode='out')
        self.NUM_V = Graph.vcount()

    def _is_cut_vertex(self, source: int, target: int, u: int):
        """
        Checks if a given vertex, u, is a cut-vertex for a given source and target.

        Parameters
        ----------
        G : ig.Graph
            Input graph
        source : int
            Number of source vertex
        target : int
            Number of target vertex
        u : int
            Number of vertex to check if it is a cut vertex

        Returns
        -------
        :bool
        True if `u` is a cut vertex of `source` and `target`
        False if `u` is not a cut vertex of `source` and `target`
        """
        G_tmp = self.Graph.copy()
        G_tmp.delete_vertices(u)

        # compensate for graph resizing
        source_tmp = source - 1 if u < source else source
        target_tmp = target - 1 if u < target else target

        if source == target:
             return False
        elif G_tmp.vertex_connectivity(source_tmp, target_tmp, neighbors="negative") == 0 and G.vertex_connectivity(source, target, neighbors="negative") != 0:
            return True
        return False

    def _alt_path_exists(self, source, target, cut_vertex):
        """
        Given a graph, source, target and cut vertex, determine if an alternating path exists. In other words check if the
        the cut vertex is protected.

        Parameters
        ----------
        G : ig.Graph
            Input graph
        source : int
            Number of source vertex
        target : int
            Number of target vertex
        cut_vertex : int
            Number of cut vertex

        Returns
        -------
        P_alt_exists : bool
            True if there is an alternating path, False otherwise.
        """
        P_alt_exists = False
        # First check if u is a cut vertex or if source and target are connected
        # if (not _is_cut_vertex(G, source, target, cut_vertex)) or G.vertex_connectivity(source, target, neighbors="ignore") == 0:
        #     return P_alt_exists
        NUM_V = self.NUM_V
        G_tmp = del_cut_edges(self.Graph, cut_vertex)

        # add the target to list containing vertices in-coming to the cut vertex
        in_cut_d = self.Graph.neighbors(cut_vertex, mode='in')
        in_cut_d.append(target)

        # if the source isn't already included, append it to make things easier. 
        # Otherwise we would need to check for a supernode that contains the source when finding a path for network H
        if source not in in_cut_d:
             in_cut_d.append(source)

        Connectivity_sets = get_Connect_Sets(G_tmp)

        # Check for intersection bewtween vertex sets, also add edges between sets that intersect
        Intersection_sets, edges_H = get_intersectionSet_hEdges(Connectivity_sets, in_cut_d, NUM_V)

        # Now that we have intersection sets, make a meta graph H and find a path
        num_vertices_H = len(in_cut_d)
        H = ig.Graph(num_vertices_H, edges_H, directed=False)

        # Get a shortest path in the graph H.
        P_alt_H = H.get_shortest_paths(in_cut_d.index(source), in_cut_d.index(target))[0]
        if len(P_alt_H) > 0:
            P_alt_exists = True

        return P_alt_exists

    def _u_does_not_learn(self, source: int, target: int,  u: int):
        """
        Checks if a certain vertex can be used to securely transmit a message for a source to a target. The targets are predetermined.
        We are trying to find a set of sources that can disseminate a key to the targets.

        Parameters
        ----------
        self : ShareKey
            Current class instance
        source : int
            The source vertex.
        target : int
            The target vertex.
        u : int
            A vertex that is possibly traversed during the communication from source to target.

        Returns
        -------
        :int
        1: If there exists an alternating path or u is not a cut vertex
        0: If there does not exist an alternating path and u is a cut vertex, or the source is not connected to the target at all.
        """

        # if self.Graph.vertex_connectivity(source, target, neighbors="ignore") == 0:
        print(f"source: {source}\ttarget: {target}\tu: {u}")
        if source == u:
            print("source == u\n")
            return 0
        elif not self._is_cut_vertex(source, target, u):
            print("not cut-vertex\n")
            return 1
        elif self._alt_path_exists(source, target, u):
            print("alt path exists\n")
            return 1
        print("otherwise\n")
        return 0

    def does_scheme_exist(self):
        """
        Determines if a scheme for sharing a key exists for a network G.

        Parameters
        ----------
        self: class ShareKey
            Current class instance

        Returns
        -------
        True: If a scheme exists
        False: Otherwise
        """
        NUM_V = self.NUM_V
        NUM_POTENTIAL_CUTS = NUM_V - len(self.targets)
        # find potential sources (vertices which are connected to all targets)
        V_potential_sources = []
        V_no_targets = [] # vertices in graph excluding targets, V \ D
        for s in self.topological_order:
            if all(G.vertex_connectivity(s, t, checks=False, neighbors='negative') != 0 for t in self.targets if s != t):
                V_potential_sources.append(s)
            if s not in self.targets:
                V_no_targets.append(s)
        NUM_POTENTIAL_SOURCES = len(V_potential_sources)
        print(V_potential_sources)

        # Initialize matrix of potential sources and potential cut vertices
        m_SU = np.asmatrix( np.zeros((NUM_POTENTIAL_SOURCES, NUM_POTENTIAL_CUTS)) )

        # populate matrix
        for s in V_potential_sources:
            for u in V_no_targets:
                s_index = V_potential_sources.index(s)
                u_index = V_no_targets.index(u)
                m_SU[s_index, u_index] = 1 if all(self._u_does_not_learn(s, t, u) == 1 for t in self.targets) else 0

        # check if a vertex that is not a target learns the key
        for i in range(NUM_POTENTIAL_CUTS):
            if np.sum(m_SU[:,i]) == 0:
                return False

        print(m_SU)
        return True

class ShareSecret: 
    def __init__(self, Graph: ig.Graph, targets = None):
        self.Graph = Graph
        self.targets = targets
        self.topological_order = Graph.topological_sorting(mode='out')
        self.NUM_V = Graph.vcount()
    
    def get_Connect_Sets(self):
        """
        Creates a set for each vertex. These sets contain all of the vertices 
        that are connected to a specific vertex. For simplicity, the vertex 
        itself is included in its own set.

        Paramters
        ---------
        self
            The current class instance

        Return
        ------
        Connectivity_sets : list
        """
        V_ordered = self.Graph.topological_sorting(mode='out')
        connectivity_sets = [[] for i in range(self.NUM_V)]
        
        for i, vertex in enumerate(V_ordered):
            connectivity_sets[vertex].append(vertex)                            # append vertex to its own set
            for rest_v in V_ordered[i+1:]:                                      # iterate throw the rest of the vertices in front of the current one
                if self.Graph.are_adjacent(vertex, rest_v):                     # check if current vertex is adjacent to another vertex
                    connectivity_sets[rest_v].extend(connectivity_sets[vertex]) # append set of current vertex to other vertex, pass the set along
            connectivity_sets[vertex] = list(set(connectivity_sets[vertex]))    # get rid of diplicates in sets

        return connectivity_sets
    
    def get_Cut_Vertices(self, source: int, target: int):
        """
        Find all cut vertices in a DAG graph. Returns a list of these vertices.

        Paramters
        ---------
        source : int 
            Number of source
        target : int 
            Number of target

        Returns
        -------
        cut_vertices : list
            A list containing the cut-vertices for a source and target.
            Returns an empty list if vertices are not connected or no cut-vertex exists.
        """

        cut_vertices = []
        source_i = self.topological_order.index(source)
        target_i = self.topological_order.index(target)

        # check if source and target are already directly connected
        if self.Graph.are_adjacent(source, target):
            print("Source and target are directly connected.\nNo network scheme needed.")
            return cut_vertices

        # check if source and target are connected
        if self.Graph.vertex_connectivity(source, target, neighbors="ignore") == 0:
            print("Source is not connected to target.\n")
            return cut_vertices

        # iterate from the vertex succeeding the source to the vertex preceeding the target
        for u in self.topological_order[source_i+1:target_i]:
            G_tmp = self.Graph.copy()
            G_tmp.delete_vertices(u)

            # compensate for graph resizing
            source_tmp = source - 1 if u < source else source
            target_tmp = target - 1 if u < target else target

            # if s and t are no longer connected then u is a cut-vertex, append to list
            if G_tmp.vertex_connectivity(source_tmp, target_tmp, neighbors="ignore") == 0:
                cut_vertices.append(u)

        del G_tmp
        return cut_vertices
    
def intersection(l1: list, l2: list):
    """
    Returns the intersection of two lists.

    Parameters
    ----------
    l1: list
    l2: list

    Returns
    -------
    :list
        The intersection of l1 and l2.
    """
    return list(set(l1).intersection(l2))

def del_cut_edges(G: ig.Graph, cut_vertex: int):
    """
    Delete the incoming and outgoing edges of a vertex. In our case we want to do this with the cut vertex.

    Parameters
    ----------
    G : ig.Graph
        Input graph
    cut_vertex : int
        Identifying index of the vertex
    
    Returns
    -------
    G_tmp : ig.Graph
        Returns a copy of the input graph G with edges for `cut_vertex` removed.
    """
    G_tmp = G.copy()
    in_cut = G.neighbors(cut_vertex, mode='in')
    out_cut = G.neighbors(cut_vertex, mode='out')
    rm_edges_in = [(i, cut_vertex) for i in in_cut]
    rm_edges_out = [(cut_vertex, i) for i in out_cut]
    rm_edges = rm_edges_in + rm_edges_out
    G_tmp.delete_edges(rm_edges)
    return G_tmp


if __name__ == "__main__":
    NUM_V = 8
    s1, s2, u1, u2, w1, w2, d1, d2 = 0, 1, 2, 3, 4, 5, 6, 7
    V_label = ["s1", "s2", "u1", "u2", "w1", "w2", "d1", "d2"]
    EDGES = [(s1, u1), (s1, d2), (s2, u2), (s2, d1), (u1, d1), (u2, d2), (w1, s1), (w1, d1), (w2, s2), (w2, d2)]
    # K = Child([6, 7], NUM_V, EDGES, True)
    G = ig.Graph(NUM_V, EDGES, True)
    K = ShareSecret(G, [6, 7])
    print(K.get_Connect_Sets())
    print(K.topological_order)
    print(K.get_Cut_Vertices(s1, d1))


    fig, ax = plt.subplots()
    ig.plot(K.Graph, 
        target=ax,
        vertex_label=V_label
    )
    plt.show()