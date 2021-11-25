class DataLoader:
    def __init__(self, file_path='assignment3/dataset/web-Stanford.txt'):
        self.file_path = file_path

    def load_data(self):
        with open(self.file_path) as data:
            # iterate through each line in the file
            for line in data:
                if line[0] != '#': # ignore comment lines
                    elems = line.split()
                    from_node, to_node = int(elems[0]), int(elems[1])
                    yield from_node, to_node


