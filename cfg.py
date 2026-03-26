"""
config.py - Configuration and environment management for the advanced Python shell.
"""
import os
import datetime
import subprocess
import importlib

class ShellConfig:
    """Loads and manages shell configuration and environment variables."""
    def __init__(self):
        self.config = {}
    def load(self, path):
        """Load configuration from a file."""
        try:
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        self.config[k.strip()] = v.strip()
        except Exception:
            pass
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    def render_prompt(self):
        theme_name = self.get('THEME', 'default')
        try:
            theme_mod = importlib.import_module(f'unix.themes.{theme_name}')
            return theme_mod.get_prompt()
        except Exception:
            # Fallback to built-in prompt
            prompt = self.get('PROMPT')
            if not prompt:
                prompt = 'myshell:{cwd}$ '
            cwd = os.getcwd()
            now = datetime.datetime.now().strftime('%H:%M:%S')
            # Git branch detection
            git = ''
            try:
                git = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
            except Exception:
                pass
            return prompt.format(cwd=cwd, time=now, git=git) 