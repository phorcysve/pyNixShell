"""
history.py - Command history and expansion for the advanced Python shell.
"""

class HistoryManager:
    """Manages command history and history expansion (!, !!, etc.)."""
    def __init__(self):
        self.history = []
    def add(self, line):
        """Add a command to history."""
        self.history.append(line)
    def get(self, index):
        """Get a command from history by index."""
        if 0 <= index < len(self.history):
            return self.history[index]
        return None
    def expand(self, line):
        """Expand history references in a command line."""
        import re
        
        # !! -> Last command
        if '!!' in line:
            last_cmd = self.history[-1] if self.history else ''
            line = line.replace('!!', last_cmd)
        
        # !N -> Nth command (1-based)
        pattern_idx = re.compile(r'!(\d+)')
        def replace_idx(match):
            idx = int(match.group(1)) - 1
            return self.get(idx) or match.group(0)
        line = pattern_idx.sub(replace_idx, line)
        
        # !prefix -> Last command starting with prefix
        # We'll only handle !prefix at the start of a word for now to avoid too much complexity
        pattern_prefix = re.compile(r'!([a-zA-Z_][a-zA-Z0-9_]*)')
        def replace_prefix(match):
            prefix = match.group(1)
            for cmd in reversed(self.history):
                if cmd.startswith(prefix):
                    return cmd
            return match.group(0)
        line = pattern_prefix.sub(replace_prefix, line)
        
        return line
 