import time
import argparse
import os
from data_loader import DataLoader
from algo_lib import TriestBase, TriestImproved

# https://snap.stanford.edu/data/ego-Facebook.html


improved = [False, True]
MTest = [500,1000,2000,5000,10000]

result_base = []
result_imp = []

for imp in improved: 
    for m in MTest: 
        parser = argparse.ArgumentParser(description='Find/ estimate triangles in graph')
        parser.add_argument('-dataset-file', default= r'facebook_combined.txt', help='Path to the data file with edge per line')
        parser.add_argument('-M', default=m, type=int, help='Edge sample size for reservoir')
        parser.add_argument('-improved', default=imp, type=bool, help='Use the improved version of the algorithm')

        args = parser.parse_args()

        data_loader = DataLoader(args.dataset_file)
        if args.improved:
            start_time = time.time()
            triestImpr = TriestImproved(data_loader, args.M)
            global_triangle_estimate = triestImpr.run()
            end_time = time.time()
            print("{} Global triangles found by TRIES-IMPROVED in {} seconds".format(global_triangle_estimate, (end_time-start_time)))
            print("M used: ",m,"Diff against true count",global_triangle_estimate - 1612010)
            result_base.append(global_triangle_estimate)
            if "undir_facebook_combined" in args.dataset_file : print("1612010 is true triangle count")
        else:
            start_time = time.time()
            triestBase = TriestBase(data_loader, args.M)
            global_triangle_estimate = triestBase.run()
            end_time = time.time()
            print("{} Global triangles found by TRIES-BASE in {} seconds".format(global_triangle_estimate, (end_time-start_time)))
            print("M used: ",m,"Diff against true count",global_triangle_estimate - 1612010)
            result_imp.append(global_triangle_estimate)
            if "undir_facebook_combined" in args.dataset_file : print("1612010 is true triangle count")
        
        # for from_node, to_node in dl.load_data():
        #         print(f'edge: {from_node} -> {to_node}')