import numpy as np
import pandas as pd
import itertools
import random

class  Shingling:
    def __init__(self, k=10):
        self.k = k

    def create_shingles(self, doc, hashed=True):
        return set([self.get_shingle_hash(doc[idx:(idx + self.k)]) for idx in range(len(doc) - self.k + 1)]) # get unique shingles

    def  get_shingle_hash(self, shingle):
        return hash(shingle)
    
    def create_characteristic_matrix(self, documents):
        shingles_per_doc = []
        # create all shingles
        for doc_id, doc in enumerate(documents):
            doc_shingles_hashed = self.create_shingles(doc)    
            shingles_per_doc.append(doc_shingles_hashed)

        unique_shingles = list(set([sh for sh in list(itertools.chain(*shingles_per_doc))]))
        shingle_id_map  = {sh:idx for idx, sh in enumerate(unique_shingles)}

        num_docs, num_shingles = len(documents), len(unique_shingles)
        data = np.zeros((num_shingles,num_docs),  dtype=bool)
        for doc_id, doc_shingle_list in enumerate(shingles_per_doc):
            for sh in doc_shingle_list:
                shingle_idx = shingle_id_map.get(sh)
                data[shingle_idx][doc_id] = 1
        characteristic_matrix = pd.DataFrame(data=data,  index=list(shingle_id_map), columns=range(num_docs))
        return characteristic_matrix

class CompareSets:
    @staticmethod
    def jaccard_similarity(doc_1, doc_2):
        shingle_idx_doc_1, shingle_idx_doc_2 = doc_1[doc_1].index, doc_2[doc_2].index
        similarity = len(shingle_idx_doc_1.intersection(shingle_idx_doc_2)) / len(shingle_idx_doc_1.union(shingle_idx_doc_2))
        return similarity

class MinHashing:
    def __init__(self, matrix, num_signatures):
        self.matrix = matrix
        self.num_signatures = num_signatures

        c = 7919

        if num_signatures > c:
            print("Error")
            break

        a_len = 4
        
        a = list(range(0,a_len))
        b = list(range(0,a_len))

        for i in range(a_len):
            a[i] = random.radnint(0,num_signatures)
            b[i] = random.radnint(0,num_signatures) 
            #generate matrix 

        sign = []
        for i in range(num_signatures):

            for item in matrix:
                h = (a[i]*item + b[i])%c
            sign.append(h)

        return sign
        #h = (ax + b)%c


    
documents = ["abcab","acab", "aabcbb"]
shingler = Shingling(2)
matrix = shingler.create_characteristic_matrix(documents)
print(matrix)

cp = CompareSets()
print(cp.jaccard_similarity(matrix[:][0], matrix[:][1]))

mini = MinHashing(matrix[:][0], 2)