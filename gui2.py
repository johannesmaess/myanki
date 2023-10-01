from tkinter import *
root = Tk()

root.geometry('700x600+250+5')
fr0 = Frame(root)
fr0.grid(row=0, column=0)

Label(fr0, text="Position 1 : x=0, y=0", bg="#FFFF00", fg="white").place(x=5, y=0)
Label(fr0, text="Position 2 : x=50, y=40", bg="#3300CC", fg="white").place(x=50, y=40)
Label(fr0, text="Position 3 : x=75, y=80", bg="#FF0099", fg="white").place(x=75, y=80)

Button(fr0, text='Browse ...').grid(row=1, column=0, sticky=W)
Label(fr0, text='Choose file:').grid(row=0, column=0, sticky=W)

fr = Frame(root)
fr.grid(row=2, column=0, sticky=W)

# nested, frame as parent
entry1 = Entry(fr)
entry1.grid(row=0, column=0, sticky=W)
entry2 = Entry(fr)
entry2.grid(row=0, column=1, sticky=W)
entry2 = Entry(fr)
entry2.grid(row=1, column=1, sticky=W)
entry2.grid(row=1, column=0, sticky=W)



root.mainloop()
