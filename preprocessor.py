import os
import codecs
import string

class Preprocessor:
    def __init__(self, \
                 TEXT_DIR = "dataset/sportsArticles/raw_data", \
                 MAX_DOC_COUNT = 100, \
                 lower_case=True, \
                 norm_spaces=True, \
                 punctuation=True):
        self.TEXT_DIR = TEXT_DIR
        self.MAX_DOC_COUNT = MAX_DOC_COUNT
        self.lower_case = lower_case
        self.norm_spaces = norm_spaces
        self.punctuation = punctuation

        self.corpus = []

    def load_texts_from_dir(self):
        for count, file_name in enumerate(os.listdir(self.TEXT_DIR)):
            if count <= self.MAX_DOC_COUNT:
                file_path = self.TEXT_DIR+"/"+file_name
                with codecs.open(file_path, 'r', 'ISO-8859-1') as text_file:
                    text = reader = str(text_file.read())
                    clean_text = self.clean_text(text)
                    self.corpus.append(clean_text)

    def clean_text(self, txt):
        if self.lower_case:
            txt = txt.lower()
        if self.norm_spaces:
            txt = ' '.join(txt.split()) # split recognizes all types of whitespaces
        if self.punctuation:
            txt = ''.join(c for c in txt if c not in string.punctuation)
        return txt
