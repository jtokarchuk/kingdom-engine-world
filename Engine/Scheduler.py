import time

class Scheduler:
    def __init__(self):
        self.jobs = []

    def register(self, identifier, script, target, max=0, interval=None):
        job = Job(identifier, script, target, max, interval)
        self.jobs.append(job)

    def deregister(self, identifier):
        for job in self.jobs:
            if job.identifier == identifier:
                self.jobs.remove(job)

    def check_jobs(self):
        for job in self.jobs:
            now = int(time.time())
            last_run = int(job.last_run)
            interval = int(job.interval)

            if (now - last_run) > interval:
                # TODO: Add scripting engine to run jobs
                print(job.identifier + " should run!")
                job.last_run = now

        

class Job:
    def __init__(self, identifier, script, target, max=0, interval=None):
        self.identifier = identifier
        self.interval = interval
        self.script = script
        self.last_run = 0
        self.max = max
        self.run_count = 0

        self.target = target
