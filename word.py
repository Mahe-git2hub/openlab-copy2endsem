from app import wc

if __name__ == '__main__':
    if input('Do you want to run WordCloud. It takes around 20mins in colab to run. It might even take longer in pc '
             'and laptops? (Y/N') == 'Y':
        wc(pickle.load(open("vocab and nlp Obj.pickle", "rb")))
