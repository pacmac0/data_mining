class DataLoader:
    def __init__(self, file_path='assignment3/dataset/example.txt'):
        self.file_path = file_path

    def load_data(self):
        with open(self.file_path) as data:
            # iterate through each line in the file
            for line in data:
                if line[0] != '#': # ignore comment lines
                    elems = line.split()
                    from_node, to_node = int(elems[0]), int(elems[1])
                    # catch self-references, would lead to a lot of neighborhoods (just in case)
                    if from_node == to_node:
                        continue
                    # change all edges to one direction (for directed graphs, for undirected it wouldnt make a difference)
                    # the case that the otherdirection was already encountered will be cought in the algorithm by checking the graph sample
                    elif from_node > to_node:
                        to_node, from_node = from_node, to_node
                    yield from_node, to_node


