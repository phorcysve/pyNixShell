"""
utils.py - Utility functions for the advanced Python shell.
"""

import os
import subprocess
import re

def shell_print(msg):
    """Print a message to the shell (placeholder for advanced formatting)."""
    print(msg)

def expand_variables(line):
    """Expand environment variables in a command line."""
    # Matches $VAR or ${VAR}
    def replace_var(match):
        var_name = match.group(1) or match.group(2)
        return os.environ.get(var_name, '')
    
    line = re.sub(r'\$\{([^}]+)\}', replace_var, line)
    line = re.sub(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', replace_var, line)
    return line

def expand_command_substitution(line, shell_run_command_func=None):
    """Expand command substitutions $(...) in a command line."""
    # Matches $(command)
    pattern = re.compile(r'\$\(([^)]+)\)')
    
    def replace_cmd(match):
        cmd = match.group(1)
        try:
            # If we have a shell instance, we can use its run_command to get more accurate results
            # but for now, we'll use subprocess for simplicity to avoid circular dependencies
            # or just call it directly if it's a simple command.
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
            return output
        except Exception:
            return ''
            
    return pattern.sub(replace_cmd, line)

def expand_all(line):
    """Expand all variables and command substitutions."""
    line = expand_variables(line)
    line = expand_command_substitution(line)
    return line
 