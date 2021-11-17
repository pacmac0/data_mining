import time
import argparse
from algo_lib import Apriori

parser = argparse.ArgumentParser(description='Find frequent itemsets with Apriori')
parser.add_argument('-dataset-file', default='assignment2/dataset/T10I4D100K.dat', help='Path to the data file with bucket per line as ')
parser.add_argument('-suport', default=0.01, type=int, help='Minimum support of itemset in %')

args = parser.parse_args()

ap = Apriori(args.dataset_file, args.suport)
start_time = time.time()
ap.run()
end_time = time.time()
print(f"Ran Apriori in {round(end_time - start_time, 2)} seconds!")
print(ap.L)
