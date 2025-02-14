import igraph as ig
from .base_funcs import *

class ShareSecret:
    def __init__(self, Graph: ig.Graph, source: int, target: int):
        self.Graph = Graph
        self.source = source
        self.target = target
        self.topological_order = Graph.topological_sorting(mode='out')
        # self.paths = {}

    def get_cut_vertices(self):
        """
        Find all cut vertices in a DAG graph. Returns a list of these vertices.

        Paramters
        ---------
        - self

        Returns
        -------
        - cut_vertices : list
            - A list containing the cut-vertices for a source and target.
              Returns an empty list if vertices are not connected or no cut-vertex exists.
        """

        cut_vertices = []
        source_i = self.topological_order.index(self.source)
        target_i = self.topological_order.index(self.target)

        # check if source and target are already directly connected
        if self.Graph.are_adjacent(self.source, self.target):
            print("Source and target are directly connected.\nNo network scheme needed.")
            return cut_vertices

        # check if source and target are connected
        if self.Graph.vertex_connectivity(self.source, self.target, neighbors="ignore") == 0:
            print("Source is not connected to target.\n")
            return cut_vertices

        # iterate from the vertex succeeding the source to the vertex preceeding the target
        for u in self.topological_order[source_i+1:target_i]:
            G_tmp = self.Graph.copy()
            G_tmp.delete_vertices(u)

            # compensate for graph resizing
            source_tmp = self.source - 1 if u < self.source else self.source
            target_tmp = self.target - 1 if u < self.target else self.target

            # if s and t are no longer connected then u is a cut-vertex, append to list
            if G_tmp.vertex_connectivity(source_tmp, target_tmp, neighbors="ignore") == 0:
                cut_vertices.append(u)

        del G_tmp
        return cut_vertices

    def get_alternating_path(self, Graph_H=False):
        """
        Gets the alternating path for the graph used to initialize the graph for communication bewtween the initialized
        source and target.

        Parameters
        ----------
        - self : ShareSecret
            - The current class instance

        Returns
        -------
        - P_alt : list
            - The alternating path
        """
        

        # get all cut vertices between the source and target
        cut_vertices = self.get_cut_vertices()

        # check if any cut vertices exists or too many exist. This alorithm is only implemented for 1 cut vertex
        num_cut_vertices = len(cut_vertices)
        if num_cut_vertices != 1:
            print(f"Number of cut vertices: {num_cut_vertices}.\nAlternating path with this algorithm does not exist.")
            return
        
        # get set of incoming edges to cut vertex + source + target
        in_cut_source_target = self.Graph.neighbors(cut_vertices[0], mode='in')
        in_cut_source_target.append(self.target)
        if self.source not in in_cut_source_target:
            in_cut_source_target.append(self.source)
        
        G_tmp = del_cut_edges(self.Graph, cut_vertices[0])      # create temporary graph which disconnects the cut vertex from the original graph
        connectivity_sets = get_connect_sets(G_tmp)             # with the cut vertex removed, get the connect sets
        
        # get the intersection of the connect sets and the edges for meta graph H
        intersection_sets, edges_H = get_intersection_set_H_edges(G_tmp, connectivity_sets, in_cut_source_target)

        # make meta graph H
        H_NUM_V = len(in_cut_source_target)
        source_H = in_cut_source_target.index(self.source)
        target_H = in_cut_source_target.index(self.target)
        H = ig.Graph(H_NUM_V, edges_H)
        H.vs["name"] = range(H_NUM_V)
        H.vs[source_H]["name"] = 'S'
        H.vs[target_H]["name"] = 'T'

        # get a shortest path in the graph H
        P_alt_H = H.get_shortest_paths(source_H, target_H)[0]
        
        # check if alt path exists
        if len(P_alt_H) == 0:
            print("No alternating path exists.\n")
            return
        
        P_alt = []  # list for alternating path
        
        for i in range( len(P_alt_H) - 1 ):
            P_alt_H_to_G_curr = in_cut_source_target[P_alt_H[i]]    # covert to current vertex in Graph using path from H
            P_alt_H_to_G_next = in_cut_source_target[P_alt_H[i+1]]  # covert to next vertex in Graph using path from H
            intersection_tmp = intersection_sets[P_alt_H_to_G_curr] # intersection set for current vertex
            for j in range( len(intersection_tmp) ):
                intersection_set_tuple = intersection_tmp[j]        # get tuple j in intersection set
                if intersection_set_tuple[0] == P_alt_H_to_G_next:  # check if tuple j is the tuple associated with the next vertex 
                    if P_alt_H_to_G_curr != self.source or len(P_alt_H) == 2:   # account for starting at the source
                        P_alt.append(G_tmp.get_shortest_paths(intersection_set_tuple[1][0], P_alt_H_to_G_curr)[0])  # append the shortest path from an intersecting vertex to the current collider
                    P_alt.append(G_tmp.get_shortest_paths(intersection_set_tuple[1][0], P_alt_H_to_G_next)[0])      # append the shortest path from an intersecting vertex to the next collider

        if Graph_H:
            return P_alt, H
        else:
            return P_alt

    def get_source_to_target_path(self):
        """
        Returns a path from the source to the target if it exists

        Parameters
        ----------
        - self : ShareSecret
            - The current class instance
        
        Returns
        -------
        - source_to_target : list
            - The shortest path from the source to the target if it exists
        """
        source_to_target = self.Graph.get_shortest_paths(self.source, self.target)[0]
        
        if len(source_to_target) == 0:
            print("No path between source and target exists")
            return
        
        return source_to_target