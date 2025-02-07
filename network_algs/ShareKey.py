import igraph as ig
import numpy as np
from .network_base import *

class ShareKey:
    def __init__(self, Graph: ig.Graph, targets = None):
        self.Graph = Graph
        self.targets = targets
        self.topological_order = Graph.topological_sorting(mode='out')
        self.NUM_V = Graph.vcount()

    def _u_does_not_learn(self, source: int, target: int,  u: int):
        """
        Checks if a certain vertex can be used to securely transmit a message for a source to a target. The targets are predetermined.
        We are trying to find a set of sources that can disseminate a key to the targets.
        This is Function 1 from our discussions.

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
        elif not is_cut_vertex(self.Graph, source, target, u):
            print("not cut-vertex\n")
            return 1
        elif alt_path_exists(self.Graph, source, target, u):
            print("alt path exists\n")
            return 1
        print("otherwise\n")
        return 0

    def does_scheme_exist(self):
        """
        Determines if a scheme for sharing a key exists for a network G.
        This is Function 2 from our discussions.

        Parameters
        ----------
        self: class ShareKey
            Current class instance

        Returns
        -------
        True: If a scheme exists
        False: Otherwise
        """

        NUM_POTENTIAL_CUTS = self.NUM_V - len(self.targets)
        # find potential sources (vertices which are connected to all targets)
        V_potential_sources = []
        V_no_targets = [] # vertices in graph excluding targets, V \ D
        for s in self.topological_order:
            if all(self.Graph.vertex_connectivity(s, t, checks=False, neighbors='negative') != 0 for t in self.targets if s != t):
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

        # check if a vertex not in `targets` learns about the key
        for i in range(NUM_POTENTIAL_CUTS):
            if np.sum(m_SU[:,i]) == 0:
                return False

        print(m_SU)
        return True
