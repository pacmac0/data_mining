import numpy as np
from collections import defaultdict
import itertools

class Apriori:
    def __init__(self, data_file, support):
        self.data_file = data_file
        self.support = support
        self.C_k = defaultdict(int) #C1
        self.num_baskets = 0
        self.L = {}

    def check_support(self, item_count):
        return (item_count/self.num_baskets) >= self.support

    def ck_generate(self, prev_L, k):
        # use self joint rule https://www.hackerearth.com/blog/developers/beginners-tutorial-apriori-algorithm-data-mining-r-implementation/
        C_k = {}
        for set1 in prev_L: # each set is a tuple of itemids
            for set2 in prev_L:
                if set1[:(k-2)]==set2[:(k-2)] and set1[k-2]<set2[k-2]: # first check that k first id's are the same, second check that following id is larger(this way doubleing of sets is avoided) 
                    C_k[set1[:(k-1)]+(set2[k-2],)] = 0
        return C_k

    def run(self):
        # pass over data file, count items and save baskets for second pass 
        # instead of saving them we could read from file in second pass and convert again, but since file size allows saving in memory we make use of it
        baskets = []
        with open(self.data_file, 'r') as file:
            for basket in file:
                conv_basket = []
                for item in basket.split():
                    item = int(item)
                    self.C_k[item]+=1
                    conv_basket.append(item)
                baskets.append(conv_basket)
                self.num_baskets = len(baskets)

        # check itemsets if they match support (frequent_items L1)
        k = 1
        self.L[k] = {(item,):self.C_k[item] for item in sorted(self.C_k) if self.check_support(self.C_k[item])} # use tuple indexing as mentioned in book

        # multi pass for itemset k
        while len(self.L[k]) != 0: # as long as itemsets are frequent continue to pass
            # create candidates of next pass
            k += 1
            C_k = self.ck_generate(self.L[k-1].keys(), k) # dict of sets with length k
            # count occurence of new sets in baskets
            for basket in baskets:
                for ss in itertools.combinations(basket, k):
                    if ss in C_k:
                        C_k[ss]+=1
            # check support
            self.L[k] = {itemset:C_k[itemset] for itemset in sorted(C_k) if self.check_support(C_k[itemset])}
        # remove empty last entry, since in the last iteration none will be found
        self.L.popitem()


#Generating association rules with confidence at least c from the 
# itemsets found in the first step.

class Gen_aRules:

    def __init__(self, L, conf):
        self.conf = conf
        self.L = L
        self.rules = []

    def check_conf(self,I,j): #conf(I->J) = sup(I u J)/sup(I)
        if I/j >= self.conf: 
            print(I,j, I/j)
            return True
        else:
            return False

    def run(self):

        print(len(self.L))

        k = 1
        
        while k < len(self.L):
            print("k",k)

            keys = self.L[k+1].keys()

            print("keys",keys)
            for i in keys:
                print("i",i)
                for item in itertools.combinations(i,k):
                    for curr in i: 
                        print(curr,"key", i)
                        if curr not in item:
                            basket = self.L[k+1][i]
                            curr_item = self.L[k][item]

                            if self.check_conf(basket,curr_item):
                                self.rules.append([curr,item])
            k +=1