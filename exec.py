"""
executor.py - Command execution engine for the advanced Python shell.
"""
import subprocess
import os
import difflib

class CommandExecutor:
    """Executes parsed shell commands and scripts."""
    def execute(self, parsed_command, run_in_bg=False):
        """Execute a parsed command structure. Returns (exit status, process)."""
        # Advanced scripting constructs
        if 'function_def' in parsed_command:
            print(f"[executor] Function definition: {parsed_command['function_def']}")
            # TODO: Store and allow calling functions
            return 0, None
        if 'block' in parsed_command:
            print(f"[executor] Control flow block: {parsed_command['block']}")
            # TODO: Parse and execute block
            return 0, None
        if 'heredoc' in parsed_command:
            print(f"[executor] Here-document: {parsed_command['heredoc']}")
            # TODO: Handle here-doc input and pass to command
            return 0, None
        # Pipeline/regular command execution
        pipeline = parsed_command.get('pipeline', [])
        prev_proc = None
        procs = []
        opened_files = []
        for i, cmd in enumerate(pipeline):
            stdin = None
            stdout = None
            stderr = None
            try:
                # Input redirection
                if cmd['stdin']:
                    stdin = open(cmd['stdin'], 'r')
                    opened_files.append(stdin)
                elif prev_proc:
                    stdin = prev_proc.stdout
                # Output redirection
                if cmd['stdout']:
                    mode = 'a' if cmd.get('append') else 'w'
                    stdout = open(cmd['stdout'], mode)
                    opened_files.append(stdout)
                # Stderr redirection
                if cmd['stderr']:
                    stderr = open(cmd['stderr'], 'w')
                    opened_files.append(stderr)
                # Launch process
                # If it's the last process in the pipeline and not redirected, let it print to terminal
                is_last = (i == len(pipeline) - 1)
                proc_stdout = stdout
                if not stdout and not is_last:
                    proc_stdout = subprocess.PIPE
                
                proc = subprocess.Popen(cmd['args'], stdin=stdin, stdout=proc_stdout, stderr=stderr, preexec_fn=os.setpgrp)
                procs.append(proc)
                if prev_proc and prev_proc.stdout:
                    prev_proc.stdout.close()
                prev_proc = proc
            except FileNotFoundError:
                print(f"Command not found: {cmd['args'][0]}")
                # Suggest similar commands
                all_cmds = set()
                for p in ['/bin', '/usr/bin', '/usr/local/bin']:
                    try:
                        all_cmds.update(os.listdir(p))
                    except Exception:
                        pass
                suggestions = difflib.get_close_matches(cmd['args'][0], all_cmds, n=3)
                if suggestions:
                    print(f"Did you mean: {', '.join(suggestions)}?")
                return 127, None
            except PermissionError:
                print(f"Permission denied: {cmd['args'][0]}")
                return 126, None
            except Exception as e:
                print(f"Execution error: {e}")
                return 1, None
        # If background job, return immediately with process
        if run_in_bg and procs:
            return 0, procs[-1]
        # Wait for last process in pipeline
        status = procs[-1].wait() if procs else 0
        # Close any opened files
        for f in opened_files:
            try:
                f.close()
            except Exception:
                pass
        return status, None 