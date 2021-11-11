class  Shingling:
    def __init__(self, k=10):
        self.k = k

    def create_shingles(self, doc, hashed=True):
        if hashed:
            print(set([doc[idx:(idx + self.k)] for idx in range(len(doc) - self.k)]))
            shingles = set([self.get_shingle_hash(doc[idx:(idx + self.k)]) for idx in range(len(doc) - self.k)])
        else:
            shingles = set([doc[idx:(idx + self.k)] for idx in range(len(doc) - self.k)]) # get unique shingles
        return shingles

    def  get_shingle_hash(self, shingle):
        return hash(shingle)
    
    def get_doc_representation(self):
        print()



test = "abcab"
sh = Shingling(2)
print(sh.create_shingles(test))
