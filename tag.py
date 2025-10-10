from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from git import *

repos_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def update_branches_and_tags(*args):
    repo_path = os.path.join(repos_dir, repo_box.get())
    pull_repo(repo_path)
    fetch(repo_path)
    branches = get_branches(repo_path)
    tags = get_tags(repo_path)
    
    branch_box['values'] = branches
    update_commit_list()
    tag_box['values'] = [t for t in tags if "env" in t]
    update_tag_commit_display()

def update_commit_list(*args):
    commit_listbox.delete(0, tk.END)
    repo_path = os.path.join(repos_dir, repo_box.get())
    checkout_branch(repo_path, branch_box.get())
    commits = get_commits(repo_path, branch_box.get())
    search_text = search_var.get().lower()
    filtered_commits = [c for c in commits if search_text in c.lower()]
    for commit in filtered_commits:
        commit_listbox.insert(tk.END, commit)

def update_tag_commit_display(*args):
    repo_path = os.path.join(repos_dir, repo_box.get())
    commit_info = get_commit_for_tag(repo_path, tag_box.get())
    tag_commit_var.set(commit_info if commit_info else "Onbekende commit")

def copy_tag_commit_to_clipboard():
    commit_info = tag_commit_var.get()
    window.clipboard_clear()
    window.clipboard_append(commit_info)
    window.update()
    messagebox.showinfo("Gekopieerd", "Commit-informatie is gekopieerd naar het klembord.")

def move_and_push_tag():
    repo_path = os.path.join(repos_dir, repo_box.get())
    tag = tag_box.get()
    selection = commit_listbox.curselection()
    if not tag or not selection:
        messagebox.showwarning("Selectie", "Selecteer een tag en een commit.")
        return
    commit_line = commit_listbox.get(selection[0])
    commit_hash = commit_line.split(" - ")[0]
    response = messagebox.askyesno("Form", f"do you want to continue move the tag '{tag}' to commit '{commit_line}'?", icon ='question')
    if response:
        taggingMessage = askstring('tagging message', 'Give a message for the tagging')
        move = move_tag(repo_path, tag, commit_hash, taggingMessage)
        if move.startswith("ERROR"):
            messagebox.showerror("Fout", move)
        else:
            messagebox.showinfo("Succes", f"Tag '{tag}' moved to: '{commit_line}'")
            update_tag_commit_display()

        push = push_tag(repo_path, tag)
        if push.startswith("ERROR"):
            messagebox.showerror("Fout bij pushen", push)
        else:
            messagebox.showinfo("Tag gepusht", f"Tag '{tag}' is geforceerd gepusht naar origin.")

window = Tk()
window.title("Welcome to The Tag Mover")
# --- Bovenste gedeelte: Comboboxen in top_frame ---
top_frame = Frame(window)
top_frame.pack(anchor='nw', padx=10, pady=(10, 0))

search_var = tk.StringVar()
tag_commit_var = tk.StringVar()

# Combobox 1
ttk.Label(top_frame, text="select Git repo:").grid(column=0, row=0, sticky='w', padx=5, pady=5)
repo_box = ttk.Combobox(top_frame, values=get_git_repos(repos_dir), state="readonly")
repo_box.grid(column=1, row=0, sticky='w')
repo_box.bind("<<ComboboxSelected>>", update_branches_and_tags)

# Combobox 2
ttk.Label(top_frame, text="select branch:").grid(column=0, row=1, sticky='w', padx=5, pady=5)
branch_box = ttk.Combobox(top_frame, values=get_branches(os.path.join(repos_dir, repo_box.get())), state="readonly")
branch_box.grid(column=1, row=1, sticky='w')
branch_box.bind("<<ComboboxSelected>>", update_commit_list)

ttk.Label(top_frame, text="Search for commit:").grid(row=0, column=2, sticky='w',padx=(20,5))
search_entry = ttk.Entry(top_frame, textvariable=search_var)
search_entry.grid(row=0, column=3, sticky='w')
search_var.trace_add("write", lambda *_: update_commit_list())

# Combobox 3
ttk.Label(top_frame, text="select env tag:").grid(column=0, row=2, sticky='w', padx=5, pady=5)
tag_box = ttk.Combobox(top_frame, values=get_tags(os.path.join(repos_dir, repo_box.get())), state="readonly")
tag_box.grid(column=1, row=2, sticky='w')
tag_box.bind("<<ComboboxSelected>>", update_tag_commit_display)

frame_tag_info = ttk.Frame(window)
frame_tag_info.pack(anchor='nw', padx=0)
ttk.Label(frame_tag_info, text="Commit van geselecteerde tag:").pack(anchor='w', padx=5, pady=(0, 5))
tag_commit_info = ttk.Entry(frame_tag_info, textvariable=tag_commit_var, width=80, state="readonly")
tag_commit_info.pack(anchor='w', padx=5)
ttk.Button(frame_tag_info, text="📋 Kopieer", command=copy_tag_commit_to_clipboard).pack(anchor='w', padx=5)

# --- Onderste gedeelte: Listbox in apart frame ---
bottom_frame = Frame(window)
bottom_frame.pack(anchor='nw', padx=10, pady=10)

ttk.Label(bottom_frame, text="commits in branch:").pack(anchor='w', padx=5, pady=(0, 5))
commit_listbox = Listbox(bottom_frame, width=80, height=10)
commit_listbox.pack(anchor='w', padx=5)

ttk.Button(bottom_frame, text="Move and push tag", command=move_and_push_tag).pack(anchor='w', padx=5, pady=(5, 0))

window.mainloop()