import time
import argparse
from data_loader import DataLoader
from algo_lib import TriestBase

parser = argparse.ArgumentParser(description='Find/ estimate triangles in graph')
parser.add_argument('-dataset-file', default='assignment3/dataset/web-Stanford.txt', help='Path to the data file with edge per line')
parser.add_argument('-M', default=6, type=int, help='Edge sample size for reservoir')

args = parser.parse_args()

data_loader = DataLoader(args.dataset_file)
start_time = time.time()
triestBase = TriestBase(data_loader, args.M)
global_triangle_estimate = triestBase.run()
end_time = time.time()
print("{} Global triangles found in {} seconds".format(global_triangle_estimate, (end_time-start_time)))

# for from_node, to_node in dl.load_data():
#         print(f'edge: {from_node} -> {to_node}')