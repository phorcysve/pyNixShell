#!/usr/bin/env python3
"""
AI-Generated Unix-like Shell
----------------------------
A robust, feature-rich Unix shell implemented in a single Python file.
Supports pipelines, redirections, job control, history expansion,
variable expansion, and command substitution.

Features:
- Modular Class-based architecture
- Advanced Parsing (Pipes, Redirection, Backgrounding)
- Job Control (fg, bg, jobs, disown)
- Expansion Engine (Variables, Command Substitution, History)
- Built-in Commands (cd, alias, export, help, etc.)
- Interactive REPL with Tab Completion
"""

import os
import sys
import shlex
import glob
import signal
import re
import time
import subprocess
import readline
import datetime
import difflib

# ==============================================================================
# UTILS & EXPANSION ENGINE
# ==============================================================================

def shell_print(msg):
    """Utility to print messages to the shell."""
    print(msg)

class ExpansionEngine:
    """Handles all shell expansions: variables, command substitution, and history."""
    
    def __init__(self, history_manager):
        self.history = history_manager

    def expand_variables(self, line):
        """Expand environment variables like $VAR or ${VAR}."""
        def replace_var(match):
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, '')
        
        line = re.sub(r'\$\{([^}]+)\}', replace_var, line)
        line = re.sub(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', replace_var, line)
        return line

    def expand_command_substitution(self, line):
        """Expand command substitutions like $(command)."""
        pattern = re.compile(r'\$\(([^)]+)\)')
        
        def replace_cmd(match):
            cmd = match.group(1)
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
                return output
            except Exception:
                return ''
                
        return pattern.sub(replace_cmd, line)

    def expand_history(self, line):
        """Expand history references like !!, !N, and !prefix."""
        # !! -> Last command
        if '!!' in line:
            last_cmd = self.history.get_last()
            line = line.replace('!!', last_cmd)
        
        # !N -> Nth command
        pattern_idx = re.compile(r'!(\d+)')
        def replace_idx(match):
            idx = int(match.group(1)) - 1
            return self.history.get(idx) or match.group(0)
        line = pattern_idx.sub(replace_idx, line)
        
        # !prefix -> Last command starting with prefix
        pattern_prefix = re.compile(r'!([a-zA-Z_][a-zA-Z0-9_]*)')
        def replace_prefix(match):
            prefix = match.group(1)
            found = self.history.find_by_prefix(prefix)
            return found if found else match.group(0)
        line = pattern_prefix.sub(replace_prefix, line)
        
        return line

    def expand_all(self, line):
        """Apply all expansions in the correct order."""
        line = self.expand_history(line)
        line = self.expand_variables(line)
        line = self.expand_command_substitution(line)
        return line

# ==============================================================================
# CORE SHELL COMPONENTS
# ==============================================================================

class HistoryManager:
    """Manages command history."""
    def __init__(self):
        self.history = []

    def add(self, line):
        if line.strip():
            self.history.append(line)

    def get(self, index):
        return self.history[index] if 0 <= index < len(self.history) else None

    def get_last(self):
        return self.history[-1] if self.history else ''

    def find_by_prefix(self, prefix):
        for cmd in reversed(self.history):
            if cmd.startswith(prefix):
                return cmd
        return None

class CommandParser:
    """Parses shell input into executable structures."""
    
    def _split_respecting_quotes(self, line, delimiter):
        """Splits a string by delimiter while ignoring delimiters inside quotes."""
        parts, current = [], []
        in_double, in_single = False, False
        for char in line:
            if char == '"' and not in_single: in_double = not in_double
            elif char == "'" and not in_double: in_single = not in_single
            
            if char == delimiter and not in_double and not in_single:
                parts.append("".join(current).strip())
                current = []
            else:
                current.append(char)
        parts.append("".join(current).strip())
        return [p for p in parts if p]

    def parse(self, line):
        """Converts a command line into a structured dictionary."""
        # Handle parallel jobs (&)
        if '&' in line and not line.strip().endswith('&'):
            jobs = self._split_respecting_quotes(line, '&')
            if len(jobs) > 1:
                return {'parallel_jobs': [self.parse(job) for job in jobs]}
        
        # Handle wait
        if line.strip() == 'wait':
            return {'wait': True}
        
        # Handle pipeline (|)
        pipe_parts = self._split_respecting_quotes(line, '|')
        commands = []
        for part in pipe_parts:
            try:
                tokens = shlex.split(part)
            except ValueError:
                return {'pipeline': []}
            
            cmd = {'args': [], 'stdin': None, 'stdout': None, 'stderr': None, 'append': False}
            i = 0
            while i < len(tokens):
                if tokens[i] == '>':
                    cmd['stdout'], cmd['append'], i = tokens[i+1], False, i + 2
                elif tokens[i] == '>>':
                    cmd['stdout'], cmd['append'], i = tokens[i+1], True, i + 2
                elif tokens[i] == '<':
                    cmd['stdin'], i = tokens[i+1], i + 2
                elif tokens[i] == '2>':
                    cmd['stderr'], i = tokens[i+1], i + 2
                else:
                    cmd['args'].append(tokens[i])
                    i += 1
            commands.append(cmd)
        return {'pipeline': commands}

class CommandExecutor:
    """Handles execution of parsed commands, including pipelines and redirections."""
    
    def execute(self, parsed, run_in_bg=False):
        pipeline = parsed.get('pipeline', [])
        if not pipeline: return 0, None
        
        prev_proc, procs, opened_files = None, [], []
        
        for i, cmd in enumerate(pipeline):
            stdin, stdout, stderr = None, None, None
            try:
                # Redirections
                if cmd['stdin']:
                    stdin = open(cmd['stdin'], 'r')
                    opened_files.append(stdin)
                elif prev_proc:
                    stdin = prev_proc.stdout
                
                if cmd['stdout']:
                    stdout = open(cmd['stdout'], 'a' if cmd.get('append') else 'w')
                    opened_files.append(stdout)
                
                if cmd['stderr']:
                    stderr = open(cmd['stderr'], 'w')
                    opened_files.append(stderr)
                
                # Output handling for pipelines
                is_last = (i == len(pipeline) - 1)
                proc_stdout = stdout
                if not stdout and not is_last:
                    proc_stdout = subprocess.PIPE
                
                # Spawn process
                proc = subprocess.Popen(
                    cmd['args'], stdin=stdin, stdout=proc_stdout, stderr=stderr, 
                    preexec_fn=os.setpgrp
                )
                procs.append(proc)
                
                if prev_proc and prev_proc.stdout:
                    prev_proc.stdout.close()
                prev_proc = proc
                
            except FileNotFoundError:
                print(f"Command not found: {cmd['args'][0]}")
                return 127, None
            except Exception as e:
                print(f"Execution error: {e}")
                return 1, None
                
        if run_in_bg:
            return 0, procs[-1]
            
        status = procs[-1].wait() if procs else 0
        for f in opened_files: f.close()
        return status, None

class Builtins:
    """Handles internal shell commands."""
    def __init__(self):
        self.aliases = {}
        self.help_text = {
            'cd': 'Change directory', 'exit': 'Exit shell', 
            'alias': 'Set alias', 'unalias': 'Remove alias',
            'export': 'Set env var', 'unset': 'Remove env var',
            'help': 'Show this help', 'jobs': 'List jobs'
        }

    def dispatch(self, parsed, shell):
        if not parsed or 'pipeline' not in parsed or not parsed['pipeline']: return False
        args = parsed['pipeline'][0]['args']
        if not args: return False
        
        cmd = args[0]
        if cmd == 'help':
            print("\nBuilt-in commands:")
            for k, v in self.help_text.items(): print(f"  {k:<8} - {v}")
            return True
        elif cmd == 'cd':
            try: os.chdir(args[1] if len(args) > 1 else os.path.expanduser('~'))
            except Exception as e: print(f"cd: {e}")
            return True
        elif cmd == 'exit': sys.exit(0)
        elif cmd == 'alias':
            if len(args) == 1:
                for k, v in self.aliases.items(): print(f"alias {k}='{v}'")
            elif '=' in args[1]:
                k, v = args[1].split('=', 1)
                self.aliases[k] = v.strip("'\"")
            return True
        elif cmd == 'export':
            if len(args) == 2 and '=' in args[1]:
                k, v = args[1].split('=', 1)
                os.environ[k] = v
            return True
        return False

# ==============================================================================
# MAIN SHELL CLASS
# ==============================================================================

class Shell:
    def __init__(self):
        self.history = HistoryManager()
        self.expansion = ExpansionEngine(self.history)
        self.parser = CommandParser()
        self.executor = CommandExecutor()
        self.builtins = Builtins()
        self.jobs = []

    def run_command(self, line, interactive=True):
        if not line.strip(): return
        
        run_in_bg = False
        if line.strip().endswith('&'):
            run_in_bg = True
            line = line.strip()[:-1].strip()
            
        # 1. Expand (History, Vars, Command Sub)
        line = self.expansion.expand_all(line)
        
        # 2. History
        self.history.add(line)
        
        # 3. Parse
        parsed = self.parser.parse(line)
        
        # 4. Built-ins
        if self.builtins.dispatch(parsed, self): return
        
        # 5. Parallel Jobs
        if 'parallel_jobs' in parsed:
            for job in parsed['parallel_jobs']:
                self.executor.execute(job, run_in_bg=True)
            return

        # 6. Wait
        if parsed.get('wait'):
            while True:
                try: os.wait()
                except ChildProcessError: break
            return

        # 7. Execute
        status, proc = self.executor.execute(parsed, run_in_bg=run_in_bg)
        if run_in_bg and proc:
            self.jobs.append({'pid': proc.pid, 'cmd': line})

    def repl(self):
        """Main Read-Eval-Print Loop."""
        # Tab completion setup
        def completer(text, state):
            buffer = readline.get_line_buffer()
            if not buffer or ' ' not in buffer.strip():
                # Complete commands
                paths = os.environ.get('PATH', '').split(os.pathsep)
                cmds = set()
                for p in paths:
                    try: cmds.update(os.listdir(p))
                    except Exception: pass
                matches = [c for c in cmds if c.startswith(text)]
            else:
                # Complete files
                matches = glob.glob(text + '*')
            return matches[state] if state < len(matches) else None

        readline.set_completer(completer)
        readline.parse_and_bind('tab: complete')

        while True:
            try:
                cwd = os.getcwd()
                prompt = f"sh:{cwd}$ "
                line = input(prompt)
                self.run_command(line)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break

# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    shell = Shell()
    if len(sys.argv) > 1:
        # Script mode
        script_path = sys.argv[1]
        if os.path.exists(script_path):
            with open(script_path) as f:
                for line in f:
                    if line.strip() and not line.strip().startswith('#'):
                        shell.run_command(line, interactive=False)
    else:
        # Interactive mode
        shell.repl()
