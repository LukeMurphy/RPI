from multiprocessing import Process, Manager
import random
import time


def worker(shared_list, shared_dict):
  shared_list.append("hello")
  shared_dict["count"] = shared_dict.get("count", 0) + 1 
  # It adds 1 to whatever value is fetched.

def worker2(shared_list, shared_dict):
  shared_list.append("foo")
  shared_dict["count"] = shared_dict.get("count", 0) + 1 
  # It adds 1 to whatever value is fetched.

if __name__ == "__main__":
  with Manager() as manager:
    shared_list = manager.list()
    shared_dict = manager.dict()

    n = random.randint(1, 10)
    processes = [Process(target=worker, args=(shared_list, shared_dict)) for _ in range(n)]

    n = random.randint(1, 10)
    processes2 = [Process(target=worker2, args=(shared_list, shared_dict)) for _ in range(n)]

    for p in processes: p.start()
    for p in processes: p.join()

    for p in processes2: p.start()
    for p in processes2: p.join()

    while True:
      print("Final list:", list(shared_list))
      print("Final dict:", dict(shared_dict))
      print("----")
      time.sleep(2)