# Make sure the punkt tokenizer models are downloaded
import nltk
nltk.download('punkt')

import pickle
import tkinter as tk

from src.app import App
from src.app import prepare_sentence

# determine sentence
sentence = 'бабломёт Кто  знает, где дом?'
sentence = 'чи́сло'

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    app.show_front(sentence)
    root.mainloop()

