# import sys
# sys.path.append("~/Repositories/myanki/")

from src.anki import findCard, invoke
from src.morphy import parse_sentence

import tkinter as tk
import pymorphy2
import pickle
import string


def select(data):
    fields1 = ['cardId', 'factor', 'interval', 'note', 'type', 'queue', 'due', 'reps', 'lapses', 'left', 'mod']
    fields2 = ['Word', 'Meaning']
    dic = {key: data[key] for key in fields1}
    dic.update({key: data['fields'][key]['value'] for key in fields2})
    return dic

def prepare_sentence(sentence, morph, trans_trie, verbose=False):
    sentence_parsed = parse_sentence(sentence, morph)
    
    result = []
    
    for word, parsings in sentence_parsed.items():
        # for every word we try four thing (until we suceed):
        # 1. check if word (unnormalised) is in ANKI.
        # 2. normalise the word, check if normalised word is in ANKI.
        # 3. check if the word (unnormalised) is in translation table.
        # 4. check if the normalised word is in translation table.
        # 5. give up (later: use translation api).
        
        trans, hit, data = None, None, None
        
        word_lower = word.lower()
        if verbose: print(f'{word}, using {word_lower}')
    
        # 1. check if word (unnormalised) is in ANKI.
        if (word in string.punctuation):
            pass
        elif (res := findCard(word_lower)):
            hit = 'ANKI'
            trans, data = res
            data = select(data)
        else:
            for (normal, pos), parse in parsings.items():
                if verbose: print(f'{word} trying with {normal}')
                # 2. normalise the word, check if normalised word is in ANKI.
                if (res := findCard(normal)):
                    hit = 'ANKI (normalised)'
                    trans, data = res
                    data = select(data)
                elif (res := trans_trie[word_lower]):
                    hit = 'Table'
                    trans, data = res, None
                elif (res := trans_trie[normal]):
                    hit = 'Table (normalised)'
                    trans, data = res, normal

                if hit is not None:
                    break # only use the first for now.
        
        result.append((word, trans, hit, data))
    return result

REFLECTION_DIFFICULTY = 200
DIFFICULTY_UNKNOWN = 400

def calc_sentence_difficulty(prepared_sentence):
    sentence_difficulty = 0

    for prepared_word in prepared_sentence:
        try:
            word, trans, hit, data = prepared_word
            if word in string.punctuation:
                pass
            elif hit is None:
                print(f'Warning, the word "{word}" is nor in Anki not in our dictionary.')
                # this word is not in Anki.
                sentence_difficulty += DIFFICULTY_UNKNOWN
            elif 'ANKI' in hit:
                if data['reps'] == 0:
                    # this word is in Anki but has never been seen before.
                    sentence_difficulty += DIFFICULTY_UNKNOWN
                else:
                    # this word is in Anki, estimate it's difficulty based on it's ease
                    sentence_difficulty += min(0, 3000 - data['factor'])
                    if '(normalised)' in hit:
                        # this word is not in it's base form. add some difficulty.
                        sentence_difficulty += REFLECTION_DIFFICULTY
            elif 'Table' in hit:
                # this word is not in Anki.
                sentence_difficulty += DIFFICULTY_UNKNOWN
            else:
                raise Exception(f'Unkwon source. "hit"={hit}')
        except Exception as e:
            print(prepared_word, '\ncaused:', e)

    return sentence_difficulty




class App:
    ANSWERS = {1: "Again", 2: "Hard", 3: "Good", 4: "Easy"}

    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary App")
        self.root.geometry("600x400+100+200")
        self.showing_back = False

        self.instruction = tk.Label(self.root, text="Hover over a word:")
        self.sentence_frame = tk.Frame(self.root)
        self.hint_frame = tk.Frame(self.root)
        self.buttons_frame = tk.Frame(self.root)

        self.instruction.grid(row=0, column=0)
        self.sentence_frame.grid(row=1, column=0)
        self.hint_frame.grid(row=2, column=0)
        self.buttons_frame.grid(row=3, column=0)

        self.word_labels = []
        self.hint_labels = []

        # Initialize morph engine for this runtime
        self.morph = pymorphy2.MorphAnalyzer()

        # load trie for translation
        path = 'pickle/trie_ru_en.pkl'
        with open(path, 'rb') as f:
            self.trans_trie = pickle.load(f)

        root.bind("<KeyPress>", self.on_key_press)
        
    def show_front(self, sentence):
        self.sentence = sentence
        self.sentence_data = prepare_sentence(sentence, self.morph, self.trans_trie)

        for i, word_data in enumerate(self.sentence_data):
            word_label = tk.Label(self.sentence_frame, text=word_data[0], padx=5, pady=5)
            word_label.bind("<Enter>", lambda event, w_idx=i: self.word_hover(event, w_idx))
            # word_label.bind("<Leave>", self.on_leave)
            word_label.pack(side="left")

            hint_label = tk.Label(self.hint_frame, text=".", padx=5, pady=5)
            # hint_label.bind("<Enter>", lambda event, w_idx=i: self.on_hover(event, w_idx))
            hint_label.pack(side="left")

            self.word_labels.append(word_label)
            self.hint_labels.append(hint_label)

        for i, word_data in enumerate(self.sentence_data):
            print(word_data)
            if word_data[2] is None or 'ANKI' not in word_data[2]:
                print(i)
                self.show_hint(i)

        self.viewed = [False] * len(self.sentence_data)

        self.showing_back = False

    def on_key_press(self, event):
        key = event.keysym
        if not self.showing_back:
            if key=='space':
                self.show_back()
        else:
            if key in self.ANSWERS:
                self.feedback_click(self.ANSWERS[key])



    def show_back(self):
        for w_idx in range(len(self.sentence_data)): self.show_hint(w_idx)
        self.create_buttons()
        self.showing_back = True

    def word_hover(self, event, w_idx):
        self.viewed[w_idx] = True
        self.show_hint(w_idx)
    
    def show_hint(self, w_idx):
        word, trans, source, data = self.sentence_data[w_idx]
        self.hint_labels[w_idx].config(text=trans)

    def create_buttons(self):
        self.buttons = []
        for ease, answer in self.ANSWERS.items():
            b = tk.Button(self.buttons_frame, text=answer, command=lambda ease=ease: self.feedback_click(ease))
            print(answer, b)
            b.pack(side="left", padx=10)
            self.buttons.append(b)

    def feedback_click(self, ease):
        print(ease)

        answers = []

        for i, (word, trans, source, parse) in enumerate(self.sentence_data):
            if (source is not None) and 'ANKI' in source:
                answers.append({
                    "cardId": parse["cardId"],
                    "ease": ease if not self.viewed[i] else 1
                })

        success = invoke('answerCards', answers=answers)
        print(success, answers)
        # messagebox.showinfo("Feedback", f"You selected: {feedback}")

