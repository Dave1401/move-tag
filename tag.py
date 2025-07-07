import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

def is_git_repo(path):
    return os.path.isdir(os.path.join(path, ".git"))

def get_git_repos(base_path):
    return [d for d in os.listdir(base_path) if is_git_repo(os.path.join(base_path, d))]

def run_git_command(repo_path, args):
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr.strip()}"

def get_branches(repo_path):
    output = run_git_command(repo_path, ["branch", "-a", "--format=%(refname:short)"])
    return [b.strip() for b in output.splitlines() if b] if not output.startswith("ERROR") else []

def get_tags(repo_path):
    output = run_git_command(repo_path, ["tag"])
    return output.splitlines() if not output.startswith("ERROR") else []

def get_commits(repo_path, branch):
    output = run_git_command(repo_path, ["log", branch, "--pretty=format:%h - %s"])
    return output.splitlines() if not output.startswith("ERROR") else []

def checkout_branch(repo_path, branch):
    return run_git_command(repo_path, ["checkout", branch])

def move_tag(repo_path, tag, commit_hash):
    return run_git_command(repo_path, ["tag", "-f", tag, commit_hash])

def push_tag(repo_path, tag):
    return run_git_command(repo_path, ["push", "origin", "-f", tag])

def get_commit_for_tag(repo_path, tag):
    hash_output = run_git_command(repo_path, ["rev-list", "-n", "1", tag])
    if hash_output.startswith("ERROR") or not hash_output:
        return None
    message_output = run_git_command(repo_path, ["log", "-1", "--pretty=format:%s", hash_output])
    return f"{hash_output} - {message_output}"

# GUI logica
script_dir = os.path.dirname(os.path.abspath(__file__))
repos = get_git_repos(script_dir)

root = tk.Tk()
#root.withdraw()
root.title("Git Tag Verplaatser")
root.geometry("750x440")

repo_var = tk.StringVar()
branch_var = tk.StringVar()
tag_var = tk.StringVar()
tag_commit_var = tk.StringVar()
search_var = tk.StringVar()
filtered_commits = []

def update_branches_and_tags(*args):
    repo_name = repo_var.get()
    repo_path = os.path.join(script_dir, repo_name)
    branches = get_branches(repo_path)
    tags = get_tags(repo_path)
    branch_dropdown['values'] = branches
    tag_dropdown['values'] = tags
    if branches:
        branch_var.set(branches[0])
        update_commit_list()
    if tags:
        tag_var.set(tags[0])
        update_tag_commit_display()

def update_commit_list(*args):
    global filtered_commits
    commit_listbox.delete(0, tk.END)
    repo_name = repo_var.get()
    branch = branch_var.get()
    repo_path = os.path.join(script_dir, repo_name)
    checkout_branch(repo_path, branch)
    commits = get_commits(repo_path, branch)
    search_text = search_var.get().lower()
    filtered_commits = [c for c in commits if search_text in c.lower()]
    for commit in filtered_commits:
        commit_listbox.insert(tk.END, commit)

def move_selected_tag():
    repo_name = repo_var.get()
    repo_path = os.path.join(script_dir, repo_name)
    tag = tag_var.get()
    selection = commit_listbox.curselection()
    if not tag or not selection:
        messagebox.showwarning("Selectie", "Selecteer een tag en een commit.")
        return
    commit_line = commit_listbox.get(selection[0])
    commit_hash = commit_line.split(" - ")[0]
    result = move_tag(repo_path, tag, commit_hash)
    if result.startswith("ERROR"):
        messagebox.showerror("Fout", result)
    else:
        update_tag_commit_display()
        messagebox.showinfo("Succes", f"Tag '{tag}' verplaatst naar {commit_hash}")

def push_selected_tag():
    repo_name = repo_var.get()
    repo_path = os.path.join(script_dir, repo_name)
    tag = tag_var.get()
    if not tag:
        messagebox.showwarning("Selectie", "Selecteer een tag om te pushen.")
        return
    result = push_tag(repo_path, tag)
    if result.startswith("ERROR"):
        messagebox.showerror("Fout bij pushen", result)
    else:
        messagebox.showinfo("Tag gepusht", f"Tag '{tag}' is geforceerd gepusht naar origin.")

def update_tag_commit_display(*args):
    repo_name = repo_var.get()
    tag = tag_var.get()
    repo_path = os.path.join(script_dir, repo_name)
    commit_info = get_commit_for_tag(repo_path, tag)
    tag_commit_var.set(commit_info if commit_info else "Onbekende commit")

def copy_tag_commit_to_clipboard():
    commit_info = tag_commit_var.get()
    root.clipboard_clear()
    root.clipboard_append(commit_info)
    root.update()
    messagebox.showinfo("Gekopieerd", "Commit-informatie is gekopieerd naar het klembord.")

# GUI layout
top_frame = ttk.Frame(root)
top_frame.pack(padx=10, pady=10, fill='x')

ttk.Label(top_frame, text="Selecteer een Git-repo:").grid(row=0, column=0, sticky='w')
repo_dropdown = ttk.Combobox(top_frame, textvariable=repo_var, values=repos, state="readonly")
repo_dropdown.grid(row=0, column=1, sticky='w')
repo_dropdown.bind("<<ComboboxSelected>>", update_branches_and_tags)

ttk.Label(top_frame, text="Selecteer een branch (ook remotes):").grid(row=1, column=0, sticky='w')
branch_dropdown = ttk.Combobox(top_frame, textvariable=branch_var, state="readonly")
branch_dropdown.grid(row=1, column=1, sticky='w')
branch_dropdown.bind("<<ComboboxSelected>>", update_commit_list)

ttk.Label(top_frame, text="Selecteer een tag:").grid(row=2, column=0, sticky='w')
tag_dropdown = ttk.Combobox(top_frame, textvariable=tag_var, state="readonly")
tag_dropdown.grid(row=2, column=1, sticky='w')
tag_dropdown.bind("<<ComboboxSelected>>", update_tag_commit_display)

frame_tag_info = ttk.Frame(top_frame)
frame_tag_info.grid(rowspan=3,columnspan=3, sticky='w')
ttk.Label(frame_tag_info, text="Commit van geselecteerde tag:").grid(row=1, column=0, sticky='w')
tag_commit_entry = ttk.Entry(frame_tag_info, textvariable=tag_commit_var, width=80, state="readonly")
tag_commit_entry.grid(row=2, columnspan=3, sticky='w')
ttk.Button(frame_tag_info, text="📋 Kopieer", command=copy_tag_commit_to_clipboard).grid(row=3, column=0, sticky='w')

ttk.Label(top_frame, text="Filter commits:").grid(row=7, column=0, sticky='w')
search_entry = ttk.Entry(top_frame, textvariable=search_var)
search_entry.grid(row=8, column=0, sticky='w')
search_var.trace_add("write", lambda *_: update_commit_list())

ttk.Label(top_frame, text="Commits in branch:").grid(row=9, column=0, sticky='w')
commit_listbox = tk.Listbox(top_frame, width=80, height=10)
commit_listbox.grid(row=10, columnspan=3, sticky='w')

ttk.Button(top_frame, text="Verplaats tag naar geselecteerde commit", command=move_selected_tag).grid(row=11, columnspan=2, sticky='w')
ttk.Button(top_frame, text="Push tag naar origin (force)", command=push_selected_tag).grid(row=11, column=1, sticky='w')

root.update_idletasks()
root.deiconify()
root.mainloop()
