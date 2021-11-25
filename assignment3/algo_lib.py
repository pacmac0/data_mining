import random
import itertools
from collections import defaultdict

class Sample:
    def __init__(self):
        self.edges = set()
        self.adj_list = defaultdict(set) # TODO change naming

class TriestBase:
    """ Only works for insertion """
    def __init__(self, data_provider, M=6):
        self.data_provider = data_provider
        self.M = M
        self.global_counter = 0
        self.local_counters = defaultdict(int)
        self.S = 

    def sampleEdge(self, u, v, t):
        if t <= self.M: return True
        elif random.random() < self.M/t: # coin flip
            # get random edge
            # remove edge from sample
            # update counters -
            return True
        else
            return False

    def updateCounters(self, operator, u, v):

        return 110

    def run(self):
        t = 0
        for u, v in edge_stream:
            t+=1

            if self.sampleEdge(u,v,t)
                # add esge to sample
                # update counters +

        return 11