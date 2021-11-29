import time
import argparse
from data_loader import DataLoader
from algo_lib import TriestBase, TriestImproved

# https://snap.stanford.edu/data/ego-Facebook.html

parser = argparse.ArgumentParser(description='Find/ estimate triangles in graph')
parser.add_argument('-dataset-file', default='assignment3/dataset/undir_facebook_combined.txt', help='Path to the data file with edge per line')
parser.add_argument('-M', default=5000, type=int, help='Edge sample size for reservoir')
parser.add_argument('-improved', default=False, type=bool, help='Use the improved version of the algorithm')

args = parser.parse_args()

data_loader = DataLoader(args.dataset_file)
if args.improved:
    start_time = time.time()
    triestImpr = TriestImproved(data_loader, args.M)
    global_triangle_estimate = triestImpr.run()
    end_time = time.time()
    print("{} Global triangles found by TRIES-IMPROVED in {} seconds".format(global_triangle_estimate, (end_time-start_time)))
    if "undir_facebook_combined" in args.dataset_file : print("1612010 is true triangle count")
else:
    start_time = time.time()
    triestBase = TriestBase(data_loader, args.M)
    global_triangle_estimate = triestBase.run()
    end_time = time.time()
    print("{} Global triangles found by TRIES-BASE in {} seconds".format(global_triangle_estimate, (end_time-start_time)))
    if "undir_facebook_combined" in args.dataset_file : print("1612010 is true triangle count")

# for from_node, to_node in dl.load_data():
#         print(f'edge: {from_node} -> {to_node}')