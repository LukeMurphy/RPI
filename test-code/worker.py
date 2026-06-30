import threading
import queue
from multiprocessing import Process, Manager
import random
import time

def workerFcu(args):
    _q = args 
    while True:
        item = _q.get()
        print(f'Working on {item}')
        # print(f'Finished {item}')
        if item == 2 :
            _q.task_done()

def workerManagedClient(shared_list, shared_dict, id):
    shared_list.append("hello")
    shared_dict["count"] = shared_dict.get("count", 0) + 1 

    while True:
        print(f"worker {id}...{shared_list} {shared_dict['count']}")
        if random.random() < .05 :
            shared_list.append("foo")
        time.sleep(2)
