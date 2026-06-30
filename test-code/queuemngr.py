import threading
import queue
import random
from torch import rand
from worker import workerFcu

q = queue.Queue()

def _worker(args):
    _q = args
    while True:
        item = _q.get()
        print(f'Working on {item}')
        # print(f'Finished {item}')
        _q.task_done()

# Turn-on the worker thread.
threading.Thread(target=workerFcu, args = [q,],daemon=True).start()

# Send thirty task requests to the worker.
itemList = []
num = 3
for item in range(num):
    itemList.append(item)

random.shuffle(itemList)
for item in range(num):
    q.put(itemList[item])

# Block until all tasks are done.
q.join()
print('All work completed')