"""
git_completion.py - Sample plugin for git command tab completion.
"""
from . import PluginBase

git_subcommands = [
    'add', 'bisect', 'branch', 'checkout', 'clone', 'commit', 'diff', 'fetch', 'grep', 'init', 'log', 'merge',
    'mv', 'pull', 'push', 'rebase', 'reset', 'rm', 'show', 'status', 'tag'
]

def git_completer(text, state):
    matches = [cmd for cmd in git_subcommands if cmd.startswith(text)]
    try:
        return matches[state]
    except IndexError:
        return None

class Plugin(PluginBase):
    def activate(self, shell):
        print("[GitCompletion] Plugin activated!")
        if 'completion' in shell:
            shell['completion'].register('git', git_completer) 