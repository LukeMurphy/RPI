from multiprocessing import shared_memory, Process
import numpy as np

def worker(name, shape):
  # Attach to existing shared memory
  shm = shared_memory.SharedMemory(name=name)
  arr = np.ndarray(shape, dtype=np.int64, buffer=shm.buf)
  arr *= 2  # double all values
  shm.close()

if __name__ == "__main__":
  # Create a numpy array in shared memory
  shm = shared_memory.SharedMemory(create=True, size=5 * 8)  # 5 int64 = 40 bytes
  arr = np.ndarray((5,), dtype=np.int64, buffer=shm.buf)
  arr[:] = [1, 2, 3, 4, 5]

  print("Before:", arr)

  p = Process(target=worker, args=(shm.name, arr.shape))
  p.start(); p.join()

  print("After:", arr)

  shm.close()
  shm.unlink()
from multiprocessing import shared_memory, Process
import numpy as np

def worker(name, shape):
  # Attach to existing shared memory
  shm = shared_memory.SharedMemory(name=name)
  arr = np.ndarray(shape, dtype=np.int64, buffer=shm.buf)
  arr *= 2  # double all values
  shm.close()

if __name__ == "__main__":
  # Create a numpy array in shared memory
  shm = shared_memory.SharedMemory(create=True, size=5 * 8)  # 5 int64 = 40 bytes
  arr = np.ndarray((5,), dtype=np.int64, buffer=shm.buf)
  arr[:] = [1, 2, 3, 4, 5]

  print("Before:", arr)

  p = Process(target=worker, args=(shm.name, arr.shape))
  p.start(); p.join()

  print("After:", arr)

  shm.close()
  shm.unlink()
