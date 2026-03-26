"""
test_shell.py - Test suite for the advanced Python shell.
"""
import unittest
from parser import CommandParser
from shell_builtins import Builtins
from plugins import load_plugins
import tempfile
import shutil
import os

class TestShell(unittest.TestCase):
    def setUp(self):
        self.parser = CommandParser()
        self.builtins = Builtins()

    def test_parse_simple_command(self):
        parsed = self.parser.parse('ls -l')
        self.assertTrue(isinstance(parsed, dict) and 'pipeline' in parsed and isinstance(parsed['pipeline'], list))
        if not (isinstance(parsed, dict) and 'pipeline' in parsed and isinstance(parsed['pipeline'], list)):
            return
        self.assertEqual(parsed['pipeline'][0]['args'], ['ls', '-l'])

    def test_parse_pipe(self):
        parsed = self.parser.parse('ls | grep py')
        self.assertTrue(isinstance(parsed, dict) and 'pipeline' in parsed and isinstance(parsed['pipeline'], list))
        if not (isinstance(parsed, dict) and 'pipeline' in parsed and isinstance(parsed['pipeline'], list)):
            return
        self.assertEqual(len(parsed['pipeline']), 2)
        self.assertEqual(parsed['pipeline'][1]['args'], ['grep', 'py'])

    def test_parse_redirection(self):
        parsed = self.parser.parse('echo hi > out.txt')
        self.assertTrue(isinstance(parsed, dict) and 'pipeline' in parsed and isinstance(parsed['pipeline'], list))
        if not (isinstance(parsed, dict) and 'pipeline' in parsed and isinstance(parsed['pipeline'], list)):
            return
        self.assertEqual(parsed['pipeline'][0]['stdout'], 'out.txt')

    def test_builtin_cd(self):
        parsed = self.parser.parse('cd /')
        self.assertTrue(self.builtins.dispatch(parsed))

    def test_builtin_alias(self):
        parsed = self.parser.parse("alias ll='ls -l'")
        self.assertTrue(self.builtins.dispatch(parsed))
        self.assertIn('ll', self.builtins.aliases)

    def test_help(self):
        parsed = self.parser.parse('help')
        self.assertTrue(self.builtins.dispatch(parsed))

    def test_plugin_loading(self):
        # Use a temporary directory for plugins to avoid read-only errors
        temp_dir = tempfile.mkdtemp()
        try:
            # Create a dummy plugin file with a Plugin class
            plugin_code = """
class Plugin:
    def activate(self, shell):
        pass
"""
            plugin_path = os.path.join(temp_dir, 'dummy_plugin.py')
            with open(plugin_path, 'w') as f:
                f.write(plugin_code)
            plugins = load_plugins({}, plugins_dir=temp_dir)
            self.assertIsInstance(plugins, list)
            self.assertTrue(any(type(p).__name__ == 'Plugin' for p in plugins))
        finally:
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    unittest.main() 