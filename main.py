import preprocessor
import algo_lib

def main():
    pre_proc = preprocessor()
    shingler = algo_lib.Shingling()


    texts = pre_proc.load_texts_from_dir()




if __name__ == '__main__':
    main()