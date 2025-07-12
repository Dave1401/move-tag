from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Welcome to LikeGeeks app")
window.geometry("600x400")

# Container voor de bovenste selectievelden
top_frame = Frame(window)
top_frame.pack(anchor='nw', padx=10, pady=10)

# Rij 1: Label + Combobox
row1 = Frame(top_frame)
row1.pack(anchor='w', pady=5)
ttk.Label(row1, text="select:").pack(side='left', padx=5)
repo_box1 = ttk.Combobox(row1, values=["A", "B", "C"], state="readonly")
repo_box1.pack(side='left')

# Rij 2
row2 = Frame(top_frame)
row2.pack(anchor='w', pady=5)
ttk.Label(row2, text="select:").pack(side='left', padx=5)
repo_box2 = ttk.Combobox(row2, values=["A", "B", "C"], state="readonly")
repo_box2.pack(side='left')

# Rij 3
row3 = Frame(top_frame)
row3.pack(anchor='w', pady=5)
ttk.Label(row3, text="select:").pack(side='left', padx=5)
repo_box3 = ttk.Combobox(row3, values=["A", "B", "C"], state="readonly")
repo_box3.pack(side='left')

# Onderste listbox gedeelte
bottom_frame = Frame(window)
bottom_frame.pack(anchor='nw', padx=10, pady=10)

ttk.Label(bottom_frame, text="list:").pack(anchor='w', padx=5, pady=(0, 5))
commit_listbox = Listbox(bottom_frame, width=80, height=10)
commit_listbox.pack(anchor='w', padx=5)

window.mainloop()
