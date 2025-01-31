import igraph as ig

class ShareBase(ig.Graph):

    def __init__(self, n=0, edges=None, directed=True):
        super().__init__(n, edges, directed)
        self.NUM_V = n

    def del_cut_edges(self, cut_vertex: int):
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
        G_tmp = self.copy()
        in_cut = self.neighbors(cut_vertex, mode='in')
        out_cut = self.neighbors(cut_vertex, mode='out')
        rm_edges_in = [(i, cut_vertex) for i in in_cut]
        rm_edges_out = [(cut_vertex, i) for i in out_cut]
        rm_edges = rm_edges_in + rm_edges_out
        G_tmp.delete_edges(rm_edges)
        return G_tmp

    def is_cut_vertex(self, source: int, target: int, u: int):
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
        G_tmp = self.copy()
        G_tmp.delete_vertices(u)
        # compensate for graph resizing
        source_tmp = source - 1 if u < source else source
        target_tmp = target - 1 if u < target else target
        if source == target:
             return False
        elif G_tmp.vertex_connectivity(source_tmp, target_tmp, neighbors="negative") == 0 and \
            self.vertex_connectivity(source, target, neighbors="negative") != 0:
            return True
        return False
    
    def get_connect_sets(self):
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
        V_ordered = self.topological_sorting(mode='out')
        connectivity_sets = [[] for i in range(self.NUM_V)]
        for i, vertex in enumerate(V_ordered):
            connectivity_sets[vertex].append(vertex)                            # append vertex to its own set
            for rest_v in V_ordered[i+1:]:                                      # iterate throw the rest of the vertices in front of the current one
                if self.are_adjacent(vertex, rest_v):                           # check if current vertex is adjacent to another vertex
                    connectivity_sets[rest_v].extend(connectivity_sets[vertex]) # append set of current vertex to other vertex, pass the set along
            connectivity_sets[vertex] = list(set(connectivity_sets[vertex]))    # get rid of diplicates in sets
        return connectivity_sets
    
    def get_intersection_set_H_edges(self, connectivity_sets: list, in_cut_d: list):
        """
        Generate the intersecting sets for the graph and create list connecting sets that intersect.

        Parameters
        ----------
        Connectivity_sets : list
            List of connect sets
        in_cut_d : list
            List with source + incoming vertices to cut vertex + destination/target

        Returns
        -------
        Intersection_sets : list
            List of the intersection of connect sets
        edges_H : list
            List creating edges between connect sets that intersect
        """
        # Check for intersection bewtween vertex sets, also add edges between sets that intersect
        edges_H = []
        Intersection_sets = [[] for i in range(self.NUM_V)]
        for i in in_cut_d:
            for j in in_cut_d:
                intersect = intersection(connectivity_sets[i], connectivity_sets[j])
                if len(intersect) > 0 and (i != j):
                    if (in_cut_d.index(j), in_cut_d.index(i)) not in edges_H:
                        edges_H.append((in_cut_d.index(i), in_cut_d.index(j)))

                    d = (j, intersect)
                    Intersection_sets[i].append(d)
    
        return Intersection_sets, edges_H

    def alt_path_exists(self, source, target, cut_vertex):
        """
        Given a graph, source, target and cut vertex, determine if an alternating path exists. In other words check if the
        the cut vertex is protected.
        Parameters
        ----------
        Graph : ig.Graph
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
        G_tmp = self.del_cut_edges(cut_vertex)
        
        # add the target to list containing vertices in-coming to the cut vertex
        in_cut_d = self.Graph.neighbors(cut_vertex, mode='in')
        in_cut_d.append(target)
        
        # if the source isn't already included, append it to make things easier. 
        # Otherwise we would need to check for a supernode that contains the source when finding a path for network H
        if source not in in_cut_d:
             in_cut_d.append(source)
        Connectivity_sets = self.get_connect_sets(G_tmp)
        
        # Check for intersection bewtween vertex sets, also add edges between sets that intersect
        Intersection_sets, edges_H = self.get_intersection_set_H_edges(Connectivity_sets, in_cut_d, NUM_V)
        
        # Now that we have intersection sets, make a meta graph H and find a path
        num_vertices_H = len(in_cut_d)
        H = ig.Graph(num_vertices_H, edges_H, directed=False)
        
        # Get a shortest path in the graph H.
        P_alt_H = H.get_shortest_paths(in_cut_d.index(source), in_cut_d.index(target))[0]
        if len(P_alt_H) > 0:
            P_alt_exists = True
        return P_alt_exists
    
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
