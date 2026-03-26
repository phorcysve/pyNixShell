"""
completion.py - Tab and custom completion for the advanced Python shell.
"""
import os
import glob

class CompletionEngine:
    """Provides tab and custom completion for commands and files."""
    def __init__(self, custom_completions=None):
        self.custom_completions = custom_completions or {}
    def complete(self, text, state):
        # Use custom completion if available for the command
        import readline
        buffer = readline.get_line_buffer()
        line = buffer.split()
        if line and line[0] in self.custom_completions:
            matches = self.custom_completions[line[0]](text, state)
        elif len(line) <= 1:
            # Complete command names
            paths = ['/bin', '/usr/bin', '/usr/local/bin']
            cmds = set()
            for p in paths:
                try:
                    cmds.update(os.listdir(p))
                except Exception:
                    pass
            matches = [c for c in cmds if c.startswith(text)]
        else:
            # Complete file names
            matches = glob.glob(text+'*')
        try:
            return matches[state]
        except IndexError:
            return None
    def register(self, command, func):
        self.custom_completions[command] = func 