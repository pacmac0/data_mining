import random
import itertools
from collections import defaultdict

class GraphSample:
    """ build separate class to use in both variants of the algorithm """
    def __init__(self):
        self.edges = set()
        self.node_neighbors = defaultdict(set) # containes set of conected nodes for each node(key)

    def add_edge(self, u, v):
        self.edges.add((u, v))
        # running on undirected graphs so add both directions
        self.node_neighbors[u].add(v)
        self.node_neighbors[v].add(u)

    def remove_edge(self, u, v):
        self.edges.remove((u, v))
        # running on undirected graphs so remove both directions
        self.node_neighbors[u].remove(v)
        self.node_neighbors[v].remove(u)
        # check if node has no neighbors anymore after removal
        if not self.node_neighbors[u]: del self.node_neighbors[u]
        if not self.node_neighbors[v]: del self.node_neighbors[v]

    def get_edges(self):
        return list(self.edges)

    def get_node_neighbors(self, node):
        return self.node_neighbors.get(node)

    def has_node(self, node):
        return node in self.node_neighbors


    def has_edge(self, u, v):
        return (u,v) in self.edges


class TriestBase:
    """ Only works for insertion """
    def __init__(self, data_provider, M=6):
        self.data_provider = data_provider
        self.M = M
        self.global_counter = 0
        self.local_counters = defaultdict(int)
        self.graphSample = GraphSample()

    def updateCounters(self, operator, u, v):
        # check if nodes exist or neighborhood union will fail (no triangle possible since no shared neighbors)
        if not self.graphSample.has_node(u) or not self.graphSample.has_node(v): return

        u_neighbors = self.graphSample.get_node_neighbors(u)
        v_neighbors = self.graphSample.get_node_neighbors(v)
        shared_neighborhood = u_neighbors.union(v_neighbors)
        
        # update the global and local counters of the shared neighborhood
        if operator == '+':
            increment_value = 1
        else:
            increment_value = -1
        for c in shared_neighborhood:
            self.global_counter += increment_value
            self.local_counters[c] += increment_value
            self.local_counters[u] += increment_value
            self.local_counters[v] += increment_value

        # in case of decrement check for 0 values and destroy them
        if operator == '-':
            for c in itertools.chain(shared_neighborhood, (u, v)): # check nodes and their neighborhood
                if self.local_counters[c] == 0: del self.local_counters[c]

    def sampleEdge(self, u, v, t):
        """ check if sample should be updated """
        if t <= self.M: return True
        elif random.random() < self.M/t: # coin flip
            # get random edge
            a, b = random.choice(self.graphSample.get_edges())
            # remove edge from sample
            self.graphSample.remove_edge(a,b)
            # update counters -
            self.updateCounters('-', u, v)
            return True
        else:
            return False

    def run(self):
        t = 0
        for u, v in self.data_provider.load_data():
            # TODO check if edge is already present in the graphSample?
            if self.graphSample.has_edge(u, v):
                continue


            t+=1
            if self.sampleEdge(u,v,t):
                # add edge to sample
                self.graphSample.add_edge(u,v)
                # update counters +
                self.updateCounters('+', u, v)
        
        # get etimate for global triangles
        eta_t = max( 1, t*(t-1)*(t-2) / (self.M*(self.M-1)*(self.M-2)) )
        global_triangles = int(eta_t * self.global_counter)
        return global_triangles