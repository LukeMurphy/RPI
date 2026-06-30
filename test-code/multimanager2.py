from multiprocessing import Process, Value, Array

def worker(num, arr):
  num.value += 1
  for i in range(len(arr)):
    arr[i] *= -1

if __name__ == "__main__":
  num = Value('i', 0)
  arr = Array('i', [1, 2, 3])
  p = Process(target=worker, args=(num, arr))
  p.start(); p.join()
  print("num:", num.value)    # 1
  print("arr:", arr[:])       # [-1, -2, -3]