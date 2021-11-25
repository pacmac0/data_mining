import random
import itertools
from collections import defaultdict

class GraphSample:
    def __init__(self):
        self.edges = set()
        self.node_neighbors = defaultdict(set) # containes set of conected nodes for each node(key)

    def add_edge(self, u, v):
        self.edges.add((u, v))
        # running on undirected graphs so add both directions
        self.node_neighbors[u].add(v)
        self.node_neighbors[v].add(u)

    def remove_edge(self, u, v):
        self.edge_set.remove((u, v))
        # running on undirected graphs so remove both directions
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)
        # check if node has no neighbors anymore after removal
        if not self.node_neighbors[u]: del self.node_neighbors[u]
        if not self.node_neighbors[v]: del self.node_neighbors[v]

    def get_edges(self):
        return list(self.edges)


class TriestBase:
    """ Only works for insertion """
    def __init__(self, data_provider, M=6):
        self.data_provider = data_provider
        self.M = M
        self.global_counter = 0
        self.local_counters = defaultdict(int)
        self.graphSample = GraphSample()

    def updateCounters(self, operator, u, v):

        return 110

    def sampleEdge(self, u, v, t):
        if t <= self.M: return True
        elif random.random() < self.M/t: # coin flip
            # get random edge
            a, b = random.choice(self.graphSample.get_edges())
            # remove edge from sample
            self.graphSample.remove_edge(a,b)
            self.updateCounters()
            # update counters -
            return True
        else
            return False


    def run(self):
        t = 0
        for u, v in edge_stream:
            # TODO should we check if edge is already present in the graphSample?
            t+=1
            if self.sampleEdge(u,v,t)
                # add edge to sample
                self.graphSample.add_edge(u,v)
                # update counters +
                self.updateCounters('+', u, v)
        
        # get etimate for global triangles
        eta_t = max( 1, t*(t-1)*(t-2) / (self.M*(self.M-1)*(self.M-2)) )
        global_triangles = int(eta_t * self.global_counter)
        return global_triangles