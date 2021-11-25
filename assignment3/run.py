import time
import argparse
from data_loader import DataLoader
from algo_lib import TriestBase

parser = argparse.ArgumentParser(description='Find/ estimate triangles in graph')
parser.add_argument('-dataset-file', default='assignment3/dataset/web-Stanford.txt', help='Path to the data file with edge per line')
parser.add_argument('-M', default=6, type=int, help='Edge sample size')

args = parser.parse_args()

data_loader = DataLoader(args.dataset_file)
for from_node, to_node in dl.load_data():
        print(f'edge: {from_node} -> {to_node}')