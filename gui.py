import tkinter as tk
from tkinter import messagebox

class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary App")
        self.root.geometry("400x300+100+200")

        self.words = ["apple", "banana", "orange", "grape", "melon"]

        self.instruction = tk.Label(self.root, text="Hover over a word:")
        self.sentence_frame = tk.Frame(self.root)
        self.expl_frame = tk.Frame(self.root)
        self.buttons_frame = tk.Frame(self.root)

        self.instruction.grid(row=0, column=0)
        self.sentence_frame.grid(row=1, column=0)
        self.expl_frame.grid(row=2, column=0)
        self.buttons_frame.grid(row=3, column=0)

        self.word_labels = []
        self.expl_labels = []


        

        for i, word in enumerate(self.words):
            word_label = tk.Label(self.sentence_frame, text=word, padx=5, pady=5)
            word_label.bind("<Enter>", lambda event, w_idx=i: self.word_hover(event, w_idx))
            # word_label.bind("<Leave>", self.on_leave)
            word_label.pack(side="left")

            expl_label = tk.Label(self.expl_frame, text="Z", padx=5, pady=5)
            # expl_label.bind("<Enter>", lambda event, w_idx=i: self.on_hover(event, w_idx))
            expl_label.pack(side="left")

            self.word_labels.append(word_label)
            self.expl_labels.append(expl_label)



        self.create_buttons()
        self.info_boxes = []

    def word_hover(self, event, w_idx):
        print(w_idx, )
        self.expl_labels[w_idx].config(text='B')
        

    def on_hover(self, event, w_idx):
        info_box = tk.Toplevel(self.root)
        info_box.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        info_box.attributes("-topmost", True)
        info_label = tk.Label(info_box, text="AAA" + w_idx)
        info_label.pack()

        self.info_boxes.append(info_box)

    def on_leave(self, event):
        if hasattr(self, "info_box"):
            self.info_box.destroy()

    def create_buttons(self):
        button_again = tk.Button(self.buttons_frame, text="Again", command=lambda: self.handle_button_click("Again"))
        button_hard = tk.Button(self.buttons_frame, text="Hard", command=lambda: self.handle_button_click("Hard"))
        button_good = tk.Button(self.buttons_frame, text="Good", command=lambda: self.handle_button_click("Good"))
        button_easy = tk.Button(self.buttons_frame, text="Easy", command=lambda: self.handle_button_click("Easy"))

        button_again.pack(side="left", padx=10)
        button_hard.pack(side="left", padx=10)
        button_good.pack(side="left", padx=10)
        button_easy.pack(side="left", padx=10)

    def handle_button_click(self, feedback):
        messagebox.showinfo("Feedback", f"You selected: {feedback}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
