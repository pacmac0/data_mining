import argparse
from preprocessor import Preprocessor
from algo_lib import Shingling, CompareSets, MinHashing, CompareSignatures, LSH

n_docs = 15
k_shingels = 10 
n_signatures = 500
sim_treashold = 0.8
testing = True

parser = argparse.ArgumentParser(description='Find similar documents.')
parser.add_argument('-dataset-dir', default='dataset/sportsArticles/raw_data', help='path to a data directory')
parser.add_argument('-n-documents', default=n_docs, type=int, help='number of documents to read from dataset')
parser.add_argument('-k-shingles', default=k_shingels, type=int, help='construct shingles of character length k')
parser.add_argument('-n-signature', default=n_signatures, type=int, help='build a minhash signature of length n')
parser.add_argument('-sim-threshold', default=sim_treashold, type=float, help='similarity threshold for retrieving documents')
parser.add_argument('-testing', default=testing, type=bool, help='use test case')

args = parser.parse_args()

preprocessor = Preprocessor(TEXT_DIR = args.dataset_dir, \
    MAX_DOC_COUNT = args.n_documents, \
    lower_case=True, \
    norm_spaces=True, \
    punctuation=True)

print("Loading documents...")
if args.testing:
    preprocessor.load_test_cases()
else:
    preprocessor.load_texts_from_dir()
documents = preprocessor.corpus
print("Documents loaded!")

shingling = Shingling(args.k_shingles)
print("Creating characteristic matrix...")
char_matrix = shingling.create_characteristic_matrix(documents)
print("Characteristic matrix created!")


min_hashing = MinHashing(char_matrix, args.n_signature)
print("Creating signature matrix...")
signature_matrix, signature_dataframe = min_hashing.create_sig_matrix()
print("Signature matrix created!")


setComparer = CompareSets()
signatureComperer = CompareSignatures()
# create loop to compare multiple docs against each other 
if args.testing:
    compare_against_first_x = 2
else:
    compare_against_first_x = args.n_documents
for doc_id in range(compare_against_first_x): # compare eachdoc against thefirst one
    jaccard_similarity = setComparer.jaccard_similarity(char_matrix[:][0], char_matrix[:][doc_id])
    estimated_jaccard_similarity = signatureComperer.estimate_jaccard_similarity(signature_dataframe[:][0], \
                                                                                 signature_dataframe[:][doc_id])
    print("Exact similarity is: {}, estimates similarity is:{} \nDiffering by {}\n".format(jaccard_similarity, estimated_jaccard_similarity, (abs(jaccard_similarity-estimated_jaccard_similarity))))


print("Running LSH...")
lsh = LSH(signature_dataframe)
candidate_pairs = lsh.find_candidates()
for pair in candidate_pairs:
    similarity = lsh.compare_candidate(pair)
    print("DOC {} and DOC {} have similarity {}".format(pair[0], pair[1], similarity))
print("LSH finished!")
