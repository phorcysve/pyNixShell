"""
jobcontrol.py - Job and process management for the advanced Python shell.
"""
import os
import signal

class Job:
    def __init__(self, pid, command, status='Running'):
        self.pid = pid
        self.command = command
        self.status = status

class JobControl:
    """Manages background and foreground jobs, process groups, and signals."""
    def __init__(self):
        self.jobs = []
    def add_job(self, process, command):
        job = Job(process.pid, command)
        self.jobs.append(job)
        return job
    def list_jobs(self):
        for i, job in enumerate(self.jobs):
            try:
                pid, status = os.waitpid(job.pid, os.WNOHANG)
                if pid == 0:
                    job.status = 'Running'
                else:
                    job.status = f'Exited'
            except ChildProcessError:
                job.status = 'Exited'
            print(f'[{i+1}] {job.pid} {job.status} {job.command}')
    def fg(self, job_id):
        job = self.jobs[job_id-1]
        try:
            os.tcsetpgrp(0, job.pid)
        except Exception:
            pass
        os.kill(job.pid, signal.SIGCONT)
        os.waitpid(job.pid, 0)
        job.status = 'Exited'
    def bg(self, job_id):
        job = self.jobs[job_id-1]
        os.kill(job.pid, signal.SIGCONT)
        job.status = 'Running'
    def disown(self, job_id):
        job = self.jobs[job_id-1]
        self.jobs.remove(job) 