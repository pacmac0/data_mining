import random
import itertools
from collections import defaultdict

class GraphSample: # Reservoir
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
        return self.node_neighbors.get(node, set())

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
        self.t = 0

    def updateCounters(self, operator, u, v):
        # get shared neighbors of nodes
        u_neighbors = self.graphSample.get_node_neighbors(u)
        v_neighbors = self.graphSample.get_node_neighbors(v)
        shared_neighborhood = u_neighbors.intersection(v_neighbors)
        
        # update the global and local counters of the shared neighborhood
        if operator == '+':
            increment_value = 1
        else: # operator = '-'
            increment_value = -1
        for c in shared_neighborhood:
            self.global_counter += increment_value
            self.local_counters[c] += increment_value
            self.local_counters[u] += increment_value
            self.local_counters[v] += increment_value

        # in case of decrement check for empty values and destroy them
        if operator == '-':
            for c in itertools.chain(shared_neighborhood, (u, v)): # check nodes and their neighborhood
                if not self.local_counters[c]: del self.local_counters[c]

    def sampleEdge(self, u, v):
        """ check if sample should be updated """
        if self.t <= self.M: return True
        elif random.random() < self.M/self.t: # coin flip
            # get random edge
            #edges = self.graphSample.get_edges()
            a, b = random.choice(self.graphSample.get_edges())
            # remove edge from sample
            self.graphSample.remove_edge(a,b)
            # update counters -
            self.updateCounters('-', a, b)
            return True
        else:
            return False

    def run(self):
        for u, v in self.data_provider.load_data():
            if self.graphSample.has_edge(u, v):
                # the example graph is directed and has back and forth connections for nodes, 
                # we handle this by ordering the nodes of a connection and with that creating 'same entries' {(1,2)(2,1)} becomes {(1,2)(1,2)}
                # this is done to avoid the need of going through the whole dataset in an intensive preprocessing step
                # with this check, if the sample already contains the connection, we can handle this case approximately 
                # Finaly we use an !strictly! undirected dataset to avoid this problem all together "undir_facebook_combined.txt"
                print(f"Edge ({u},{v}) already in graph!")
                continue

            self.t+=1
            if self.sampleEdge(u,v):
                # add edge to sample
                self.graphSample.add_edge(u,v)
                # update counters +
                self.updateCounters('+', u, v)
        
        # get etimate for global triangles
        eta_t = max( 1, self.t*(self.t-1)*(self.t-2) / (self.M*(self.M-1)*(self.M-2)) )
        global_triangles = int(eta_t * self.global_counter)
        return global_triangles

class TriestImproved:
    """ Only works for insertion """
    def __init__(self, data_provider, M=6):
        self.data_provider = data_provider
        self.M = M
        self.global_counter = 0
        self.local_counters = defaultdict(int)
        self.graphSample = GraphSample()
        self.t = 0

    def updateCounters(self, u, v):
        # get shared neighbors of nodes
        u_neighbors = self.graphSample.get_node_neighbors(u)
        v_neighbors = self.graphSample.get_node_neighbors(v)
        shared_neighborhood = u_neighbors.intersection(v_neighbors)
        
        increment_value = max(1, (self.t-1)*(self.t-2) / (self.M*(self.M-1)))
        for c in shared_neighborhood:
            self.global_counter += increment_value
            self.local_counters[c] += increment_value
            self.local_counters[u] += increment_value
            self.local_counters[v] += increment_value

    def sampleEdge(self, u, v):
        """ check if sample should be updated """
        if self.t <= self.M: return True
        elif random.random() < self.M/self.t: # coin flip
            # get random edge
            #edges = self.graphSample.get_edges()
            a, b = random.choice(self.graphSample.get_edges())
            # remove edge from sample
            self.graphSample.remove_edge(a,b)
            # update counters - removed
            return True
        else:
            return False

    def run(self):
        for u, v in self.data_provider.load_data():
            if self.graphSample.has_edge(u, v):
                # the example graph is directed and has back and forth connections for nodes, 
                # we handle this by ordering the nodes of a connection and with that creating 'same entries' {(1,2)(2,1)} becomes {(1,2)(1,2)}
                # this is done to avoid the need of going through the whole dataset in an intensive preprocessing step
                # with this check, if the sample already contains the connection, we can handle this case approximately 
                # Finaly we use an !strictly! undirected dataset to avoid this problem all together "undir_facebook_combined.txt"
                print(f"Edge ({u},{v}) already in graph!")
                continue

            self.t+=1
            # update counters + (called unconditionally), since decrement is removed we don't need operator anymore but 't' for eta calculation
            self.updateCounters(u, v)
            if self.sampleEdge(u,v):
                # add edge to sample
                self.graphSample.add_edge(u,v)
        
        return int(self.global_counter) # since its a weighted increment we have to round to an int