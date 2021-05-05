import subprocess
import queue

class DeterministicPool():
    def __init__(self, max_concurrent=5):
        self.max_concurrent = max_concurrent

        self.tasks_pending = queue.Queue()
        self.tasks_current = []
    
    def submit(self, task):
        self.tasks_pending.put(task)

    def has_tasks(self):
        return self.tasks_pending.qsize() + len(self.tasks_current) > 0

    def tick(self):
        if not self.has_tasks(): return False

        if len(self.tasks_current) > self.max_concurrent:
            raise RuntimeError('More tasks in pool than allowed.')
        
        # Remove completed processes:
        # We gotta do this the round-about way because of race-conditions.
        task_polls = [(task, task.process.poll()) for task in self.tasks_current]
        for task, poll in task_polls:
            if poll is None:
                # This task is still executing. Do nothing.
                continue
            
            if poll != 0:
                # An error has occurred in this process.
                # Call error handler on it.
                task.on_error()
            
            if poll == 0:
                # Task completed succesfully.
                # Call the success handler.
                task.on_success()
        
        # Some processes could finish while we write,
        # and they will be handled in the next tick.
        self.tasks_current = [task_poll[0] for task_poll in task_polls if task_poll[1] is None]

        # Add new tasks
        for i in range(self.max_concurrent - len(self.tasks_current)):
            if self.tasks_pending.empty(): break

            task = self.tasks_pending.get()

            task.process = subprocess.Popen(
                task.command,
                # uncomment below line if you want stdout from created processes
                # to be printed to the Terminal
                # stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=0
            )
            
            self.tasks_current.append(task)

            task.on_launch()
        
        return True

      
class DeterministicTask():
    # Inherit from this class and implement the initialiser and hooks.
    # Pass the inherited class objects to DeterministicPool via submit()
    def __init__(self):
        pass
    
    def on_launch(self):
        raise raise NotImplementedError

    def on_success(self):
        raise NotImplementedError

    def on_error(self):
        raise NotImplementedError




        



    

