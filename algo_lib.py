import numpy as np
import pandas as pd
import itertools

class  Shingling:
    def __init__(self, k=10):
        self.k = k

    def create_shingles(self, doc, hashed=True):
        shingles = [doc[idx:(idx + self.k)] for idx in range(len(doc) - self.k + 1)] # get unique shingles
        if hashed:
            shingles_hashed = [self.get_shingle_hash(shingle) for shingle in shingles]
        return shingles, shingles_hashed

    def  get_shingle_hash(self, shingle):
        return hash(shingle)
    
    def create_characteristic_matrix(self):
        print()

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

    x = 

documents = ["abcab","acab", "aabcbb"]
shingler = Shingling(2)

shingles_per_doc = []
# create all shingles
for doc_id, doc in enumerate(documents):
    doc_shingles, doc_shingles_hashed = shingler.create_shingles(doc)    
    shingles_per_doc.append(list(zip(doc_shingles_hashed, doc_shingles)))

unique_shingles = list(set([sh for sh in list(itertools.chain(*shingles_per_doc))]))
shingle_id_map  = {sh:idx for idx, sh in enumerate(unique_shingles)}

print(shingles_per_doc)
num_docs, num_shingles = len(documents), len(unique_shingles)
data = np.zeros((num_shingles,num_docs),  dtype=bool)
for doc_id, doc_shingle_list in enumerate(shingles_per_doc):
    for sh in doc_shingle_list:
        shingle_idx = shingle_id_map.get(sh)
        data[shingle_idx][doc_id] = 1



characteristic_matrix = pd.DataFrame(data=data,  index=list(shingle_id_map), columns=range(num_docs))
print(characteristic_matrix)
# add shingles and docs to matrix

cp = CompareSets()
print( cp.jaccard_similarity(characteristic_matrix[:][0], characteristic_matrix[:][2]) )