import argparse
from preprocessor import Preprocessor
from algo_lib import Shingling, CompareSets, MinHashing, CompareSignatures, LSH
import numpy as np
import pandas as pd
from tabulate import tabulate
import time

parser = argparse.ArgumentParser(description='Find similar documents.')
parser.add_argument('-dataset-dir', default='dataset/sportsArticles/raw_data', help='path to a data directory')
parser.add_argument('-n-documents', default=15, type=int, help='number of documents to read from dataset')
parser.add_argument('-k-shingles', default=10, type=int, help='construct shingles of character length k')
parser.add_argument('-n-signature', default=1000, type=int, help='build a minhash signature of length n')
parser.add_argument('-sim-threshold', default=0.8, type=float, help='similarity threshold for retrieving documents')
parser.add_argument('-comp-matrix', default=True, type=bool, help='Compare all documents against each other')
parser.add_argument('-testing', default=True, type=bool, help='use test case')


args = parser.parse_args()

preprocessor = Preprocessor(TEXT_DIR = args.dataset_dir, \
    MAX_DOC_COUNT = args.n_documents, \
    lower_case=True, \
    norm_spaces=True, \
    punctuation=True)

print("Loading documents...")
start_time = time.time()
if args.testing:
    preprocessor.load_test_cases()
else:
    preprocessor.load_texts_from_dir()
documents = preprocessor.corpus
end_time = time.time()
print("Documents loaded in {} seconds!".format(round(end_time-start_time,3)))

shingling = Shingling(args.k_shingles)
print("Creating characteristic matrix...")
start_time = time.time()
char_matrix = shingling.create_characteristic_matrix(documents)
end_time = time.time()
print("Characteristic matrix created in {} seconds!".format(round(end_time-start_time,3)))


min_hashing = MinHashing(char_matrix, args.n_signature)
print("Creating signature matrix...")
start_time = time.time()
signature_matrix, signature_dataframe = min_hashing.create_sig_matrix()
end_time = time.time()
print("Signature matrix created in {} seconds!".format(round(end_time-start_time,3)))


setComparer = CompareSets()
signatureComperer = CompareSignatures()

print("Starting comparisons...")
start_time = time.time()
# compare all docs against each other
if args.comp_matrix:
    num_compare_docs = len(documents)
    comp_matrix = [[None for _ in range(num_compare_docs)] for _ in range(num_compare_docs)]
    for doc_id_in in range(num_compare_docs):
        for doc_id_out in range(num_compare_docs):
            jaccard_similarity = setComparer.jaccard_similarity(char_matrix[:][doc_id_in], char_matrix[:][doc_id_out])
            estimated_jaccard_similarity = signatureComperer.estimate_jaccard_similarity(signature_dataframe[:][doc_id_in], \
                                                                                        signature_dataframe[:][doc_id_out])
            comp_matrix[doc_id_in][doc_id_out] = (jaccard_similarity, estimated_jaccard_similarity)
    presenter_matrix = pd.DataFrame(comp_matrix, index=range(num_compare_docs), columns=range(num_compare_docs))
    print(tabulate(presenter_matrix, headers='keys', tablefmt='psql'))

else:
    # create loop to compare multiple docs against each other 
    if args.testing:
        compare_against_first_x = len(documents)
    else:
        compare_against_first_x = args.n_documents
    for doc_id in range(compare_against_first_x): # compare eachdoc against thefirst one
        jaccard_similarity = setComparer.jaccard_similarity(char_matrix[:][0], char_matrix[:][doc_id])
        estimated_jaccard_similarity = signatureComperer.estimate_jaccard_similarity(signature_dataframe[:][0], \
                                                                                    signature_dataframe[:][doc_id])
        print("results for document {}: \nExact similarity is: {}, estimates similarity is:{} \nDiffering by {}\n".format(doc_id, jaccard_similarity, estimated_jaccard_similarity, (abs(jaccard_similarity-estimated_jaccard_similarity))))
end_time = time.time()
print("Comparisons finnished after {} seconds!".format(round(end_time-start_time,3)))

print("Running LSH...")
start_time = time.time()
lsh = LSH(signature_dataframe)
candidate_pairs = lsh.find_candidates()
for pair in candidate_pairs:
    similarity = lsh.compare_candidate(pair)
    print("DOC {} and DOC {} have similarity {}".format(pair[0], pair[1], similarity))
end_time = time.time()
print("LSH finished after {} seconds!".format(round(end_time-start_time,3)))
