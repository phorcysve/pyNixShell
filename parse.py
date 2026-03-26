"""
parser.py - Command and script parser for the advanced Python shell.
"""
import shlex

class CommandParser:
    """Parses shell commands and scripts into executable structures."""
    def _split_respecting_quotes(self, line, delimiter):
        """Split a line by a delimiter, but ignore delimiters inside quotes."""
        parts = []
        current = []
        in_double_quote = False
        in_single_quote = False
        i = 0
        while i < len(line):
            char = line[i]
            if char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
            elif char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            
            if char == delimiter and not in_double_quote and not in_single_quote:
                parts.append("".join(current).strip())
                current = []
            else:
                current.append(char)
            i += 1
        parts.append("".join(current).strip())
        return [p for p in parts if p]

    def parse(self, line):
        """Parse a single command line or script line. Returns a parsed structure."""
        # Parallel background jobs: split on '&' (not at end)
        if '&' in line and not line.strip().endswith('&'):
            jobs = self._split_respecting_quotes(line, '&')
            if len(jobs) > 1:
                return {'parallel_jobs': [self.parse(job) for job in jobs]}
        
        # Wait command
        if line.strip() == 'wait':
            return {'wait': True}
        
        # TODO: Recognize nested blocks and function definitions
        if line.strip().startswith('function ') or ('()' in line and '{' in line):
            return {'function_def': line.strip()}
        if line.strip().startswith(('if ', 'for ', 'while ', 'case ')):
            return {'block': line.strip()}
        if '<<' in line:
            return {'heredoc': line.strip()}
            
        # Fallback: pipeline parsing
        pipe_parts = self._split_respecting_quotes(line, '|')
        commands = []
        for part in pipe_parts:
            try:
                tokens = shlex.split(part)
            except ValueError as e:
                # If shlex fails (e.g., unmatched quote), return error or fallback
                print(f"Parser error: {e}")
                return {'pipeline': []}
            
            cmd = {'args': [], 'stdin': None, 'stdout': None, 'stderr': None, 'append': False}
            i = 0
            while i < len(tokens):
                if tokens[i] == '>':
                    cmd['stdout'] = tokens[i+1]
                    cmd['append'] = False
                    i += 2
                elif tokens[i] == '>>':
                    cmd['stdout'] = tokens[i+1]
                    cmd['append'] = True
                    i += 2
                elif tokens[i] == '<':
                    cmd['stdin'] = tokens[i+1]
                    i += 2
                elif tokens[i] == '2>':
                    cmd['stderr'] = tokens[i+1]
                    i += 2
                else:
                    cmd['args'].append(tokens[i])
                    i += 1
            commands.append(cmd)
        return {'pipeline': commands} 