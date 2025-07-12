import os
import subprocess

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

def get_git_repos(base_path):
    def is_git_repo(path):
        is_git = os.path.isdir(os.path.join(path, ".git"))
        return is_git
    repos = [d for d in os.listdir(base_path) if is_git_repo(os.path.join(base_path, d))]
    return repos

def get_branches(repo_path):
    output = run_git_command(repo_path, ["branch", "-a", "--format=%(refname:short)"])
    return [b.strip() for b in output.splitlines() if b] if not output.startswith("ERROR") else []

def get_commits(repo_path, branch):
    output = run_git_command(repo_path, ["log", branch, "--pretty=format:%h - %s"])
    return output.splitlines() if not output.startswith("ERROR") else []

def get_tags(repo_path):
    output = run_git_command(repo_path, ["tag"])
    return output.splitlines() if not output.startswith("ERROR") else []

def get_commit_for_tag(repo_path, tag):
    hash_output = run_git_command(repo_path, ["rev-list", "-n", "1", tag])
    if hash_output.startswith("ERROR") or not hash_output:
        return None
    message_output = run_git_command(repo_path, ["log", "-1", "--pretty=format:%s", hash_output])
    return f"{hash_output} - {message_output}"

def checkout_branch(repo_path, branch):
    return run_git_command(repo_path, ["checkout", branch])

def pull_repo(repo_path):
    return run_git_command(repo_path, ["pull"])

def move_tag(repo_path, tag, commit_hash):
    return run_git_command(repo_path, ["tag", "-f", tag, commit_hash])

def push_tag(repo_path, tag):
    return run_git_command(repo_path, ["push", "origin", "-f", tag])