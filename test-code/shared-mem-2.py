from multiprocessing import shared_memory, Process
from multiprocessing import ShareableList

def worker(name):
  lst = ShareableList(name=name)
  lst[0] += 100
  lst.shm.close()

if __name__ == "__main__":
  sl = ShareableList([10, 20, 30])
  print("Before:", list(sl))

  p = Process(target=worker, args=(sl.shm.name,))
  p.start(); p.join()

  print("After:", list(sl))

  sl.shm.close()
  sl.shm.unlink()