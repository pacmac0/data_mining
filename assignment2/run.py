import time
import argparse
from algo_lib import Apriori, Gen_aRules
import os

appl_data = 'assignment2/dataset/T10I4D100K.dat'
win = "Documents\DM\ID2222_data_mining-main\assignment2"
parser = argparse.ArgumentParser(description='Find frequent itemsets with Apriori')
parser.add_argument('-dataset-file', default='T10I4D100K.dat', help='Path to the data file with bucket per line as ')
parser.add_argument('-suport', default=0.01, type=int, help='Minimum support of itemset in %')
parser.add_argument('-confidence', default=0.5, type=int, help='Confidence level %')

args = parser.parse_args()

print("Dir ", os.getcwd())
ap = Apriori(args.dataset_file, args.suport)
start_time = time.time()
ap.run()
end_time = time.time()
print(f"Ran Apriori in {round(end_time - start_time, 2)} seconds!")
print(ap.L)

print("Here ")

for i in ap.L:
    print(len(ap.L[i]))

#part 2

print("PART 2")
start_time = time.time()
a_rules = Gen_aRules(ap.L, args.confidence)

a_rules.run()
end_time = time.time()
for item in a_rules.rules: 
    print(item)

print(f"Ran generating assosation rules in {round(end_time - start_time, 2)} seconds!")


