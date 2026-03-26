"""
hooks_example.py - Example plugin with advanced hooks for the Python shell.
"""
from . import PluginBase

class Plugin(PluginBase):
    def activate(self, shell):
        print("[HooksExample] Plugin activated!")
        shell['pre_exec_hooks'] = shell.get('pre_exec_hooks', [])
        shell['post_exec_hooks'] = shell.get('post_exec_hooks', [])
        shell['on_error_hooks'] = shell.get('on_error_hooks', [])
        shell['pre_exec_hooks'].append(self.pre_exec)
        shell['post_exec_hooks'].append(self.post_exec)
        shell['on_error_hooks'].append(self.on_error)
    def pre_exec(self, cmd):
        print(f"[HooksExample] About to execute: {cmd}")
    def post_exec(self, cmd, status):
        print(f"[HooksExample] Finished: {cmd} (status {status})")
    def on_error(self, cmd, error):
        print(f"[HooksExample] Error in: {cmd} ({error})") 