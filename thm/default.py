"""
default.py - Default prompt theme for the advanced Python shell.
"""
import os
import datetime
import subprocess

def get_prompt():
    cwd = os.getcwd()
    now = datetime.datetime.now().strftime('%H:%M:%S')
    git = ''
    try:
        git = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        pass
    return f"myshell:{cwd} ({git}) [{now}]$ " 