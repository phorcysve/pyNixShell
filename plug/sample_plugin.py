"""
sample_plugin.py - Example plugin for the advanced Python shell.
"""
from . import PluginBase

class Plugin(PluginBase):
    def activate(self, shell):
        print("[SamplePlugin] Plugin activated!")
        # Example: add a custom command to the shell context
        shell['custom_commands'] = shell.get('custom_commands', {})
        shell['custom_commands']['hello'] = self.hello
    def hello(self, *args):
        print("Hello from SamplePlugin! Args:", args) 