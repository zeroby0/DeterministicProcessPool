# DeterministicProcessPool
A simple Deteriministic ProcessPoolExcecutor for Python 3.7+

The built-in ProcessPoolExecutor can wake processes in any order.
This one wakes them in the same order as they were submitted.

### Installation
Download the `deterministic.py` file and keep it in the same folder as the file you're importing it from.

### Usage
Here is an example to make multiple webrequests with `wget`.

```Python3
import time
from deterministic import DeterministicPool, DeterministicTask

class Task(DeterministicTask):
    def __init__(self, url):
        self.url = url

        self.command = [
            # Change this to the command you wanna run
            'wget', f'{url}'
        ]
    
    def on_launch(self):
        print(f'Started downloading {self.url}')

    def on_success(self):
        print(f'Completed downloading {self.url}')

    def on_error(self):
        print(f'Error downloading {self.url}')


if __name__ == '__main__':

    pool = DeterministicPool(max_concurrent=5)

    urls = [...] # A list of URLs you want to wget
    for url in urls:
        pool.submit(
            task = Task(
                url
            )
        )

    while pool.has_tasks():
        pool.tick()
        time.sleep(1)
        # Call pool.tick() frequently so that the pool
        # can check on the processes, and start new processes.
```

You don't need to `submit` all the tasks before hand,
you can also do that while the pool is running.

Maximum Concurrency of the pool can be increased, but cannot be decreased.
It should be trivial to implement that though, I might do that later.

### License

This library and it's documentation are [Public Domain](./LICENSE). Go nuts.
