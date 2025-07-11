# https://likegeeks.com/python-gui-examples-tkinter-tutorial/
from tkinter import *
from tkinter import ttk, messagebox

def clicked():
    lbl_repo.configure(text="Button was clicked !!")

def get_git_repos():
    return ["Repo A", "Repo B", "Repo C"]

window = Tk()

window.title("Welcome to LikeGeeks app")
window.geometry('350x200')

top_frame = ttk.Frame(window)
top_frame.pack(fill='x')

ttk.Label(top_frame, text="select repo:").grid(column=0, row=0)
repo_box = ttk.Combobox(window, values=get_git_repos(), state="readonly")
repo_box.pack()


btn = ttk.Button(top_frame, text="Click Me", command=clicked)
btn.grid(column=1, row=0)



window.mainloop()