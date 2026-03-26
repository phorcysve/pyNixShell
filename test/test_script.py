"""
test_script.py - Test running a sample script in the advanced Python shell.
"""
import subprocess
import os

def test_sample_script():
    script_path = os.path.join(os.path.dirname(__file__), '../sample_script.sh')
    shell_path = os.path.join(os.path.dirname(__file__), '../myshell.py')
    result = subprocess.run(['python3', shell_path, script_path], capture_output=True, text=True)
    output = result.stdout
    assert "Starting script..." in output
    assert "Current dir:" in output
    assert "Job 2 done" in output
    assert "help" in output or "Built-in commands:" in output 