"""
builtins.py - Built-in shell commands for the advanced Python shell.
"""
import os

class Builtins:
    """Handles built-in shell commands (cd, alias, export, etc.)."""
    def __init__(self):
        self.aliases = {}
        self.builtin_help = {
            'cd': 'Change the current directory',
            'exit': 'Exit the shell',
            'alias': 'Create or list command aliases',
            'unalias': 'Remove an alias',
            'export': 'Set an environment variable',
            'unset': 'Unset an environment variable',
            'jobs': 'List background jobs',
            'fg': 'Bring a job to the foreground',
            'bg': 'Resume a job in the background',
            'disown': 'Disown a job',
            'help': 'Show this help message',
        }
    def dispatch(self, parsed, custom_commands=None):
        # Only handle simple commands (not pipelines)
        if not parsed or 'pipeline' not in parsed or not parsed['pipeline']:
            return False
        cmd = parsed['pipeline'][0]['args']
        if not cmd:
            return False
        name = cmd[0]
        # help
        if name == 'help':
            print("\nBuilt-in commands:")
            for k, v in self.builtin_help.items():
                print(f"  {k:<8} - {v}")
            if custom_commands:
                print("\nPlugin/custom commands:")
                for k in custom_commands:
                    print(f"  {k:<8} - (plugin/custom command)")
            print()
            return True
        # cd
        if name == 'cd':
            try:
                os.chdir(cmd[1] if len(cmd) > 1 else os.path.expanduser('~'))
            except FileNotFoundError:
                print(f"cd: no such file or directory: {cmd[1] if len(cmd) > 1 else os.path.expanduser('~')}")
            except NotADirectoryError:
                print(f"cd: not a directory: {cmd[1]}")
            except PermissionError:
                print(f"cd: permission denied: {cmd[1]}")
            except Exception as e:
                print(f"cd: error: {e}")
            return True
        # exit
        if name == 'exit':
            exit(0)
        # alias
        if name == 'alias':
            if len(cmd) == 1:
                for k, v in self.aliases.items():
                    print(f"alias {k}='{v}'")
            elif '=' in cmd[1]:
                k, v = cmd[1].split('=', 1)
                v = v.strip("'\"")
                self.aliases[k] = v
            else:
                print("Usage: alias name='command'")
            return True
        # unalias
        if name == 'unalias':
            if len(cmd) == 2:
                if cmd[1] in self.aliases:
                    self.aliases.pop(cmd[1])
                else:
                    print(f"unalias: {cmd[1]}: not found")
            else:
                print("Usage: unalias name")
            return True
        # export
        if name == 'export':
            if len(cmd) == 2 and '=' in cmd[1]:
                k, v = cmd[1].split('=', 1)
                os.environ[k] = v
            else:
                print("Usage: export VAR=value")
            return True
        # unset
        if name == 'unset':
            if len(cmd) == 2:
                if cmd[1] in os.environ:
                    os.environ.pop(cmd[1])
                else:
                    print(f"unset: {cmd[1]}: not found")
            else:
                print("Usage: unset VAR")
            return True
        # jobs (stub)
        if name == 'jobs':
            print("[jobs] (job control not yet implemented)")
            return True
        # feedback
        if name == 'feedback':
            print("We value your feedback! Please open an issue at: https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/issues")
            return True
        return False 