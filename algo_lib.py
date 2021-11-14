import numpy as np
import pandas as pd
import itertools
import random
from sympy import * # https://www.geeksforgeeks.org/python-simpy-nextprime-method/

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
        self.num_shingles, self.num_docs = matrix.shape
        self.max_coef_value = len(matrix)-1 #2**32-1
        self.num_signatures = num_signatures

    def create_sig_matrix(self):
        self.matrix.reset_index(drop=True, inplace=True) # TODO: now use index instead of hash value
        sig_matrix = np.full((self.num_signatures,self.num_docs), np.inf)
        
        # create hashfunctions
        c = nextprime(self.max_coef_value)
        # coefficients a,b have to be different for each function, no acan be used double.
        a_coefficients = []
        b_coefficients = []
        # select random values in hash value range for signature hash functions
        while len(a_coefficients) <= self.num_signatures:
            a = np.random.randint(self.max_coef_value)
            if a not in a_coefficients:
                a_coefficients.append(a)
        while len(b_coefficients) <= self.num_signatures:
            b = np.random.randint(self.max_coef_value)
            if b not in b_coefficients:
                b_coefficients.append(b)

        # use for book example
        #a_coefficients = [1,3]
        #b_coefficients = [1,1]

        # compute hashfunction values
        hash_val_matrix = np.full((self.num_shingles,self.num_signatures),np.inf)
        for func_idx in range(self.num_signatures):
            for shingle_idx, shingle_hash in enumerate(self.matrix.index):
                hash_val_matrix[shingle_idx][func_idx] = (a_coefficients[func_idx]* shingle_idx + b_coefficients[func_idx]) % c # maybe use shingle_hash instead of idx
        # fill sig_matrix
        for shingle_idx, hash_vals in enumerate(hash_val_matrix):
            for doc_id in range(self.num_docs):
                if self.matrix[self.matrix.columns[doc_id]][shingle_idx]: # TODO: change indexing if hash-values are the index of the dataframe
                    sig_matrix[:, doc_id] = np.where(hash_vals < sig_matrix[:, doc_id], hash_vals, sig_matrix[:, doc_id])
                    
        sig_df = pd.DataFrame(sig_matrix, index=range(self.num_signatures), columns=self.matrix.columns)
        return sig_matrix, sig_df

    
class CompareSignatures:
    @staticmethod
    def estimate_jaccard_similarity(sig1, sig2): #signatures are columns of the sig_matrix, representing a document
        num_entries = len(sig1)
        equal_entries = (sig1 == sig2).sum()
        return equal_entries/num_entries


