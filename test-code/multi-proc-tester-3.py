from multiprocessing import Process, Queue
import time
import sys
sys.path.append("../")
from modules import configuration
from player import main


def launchPlayer(arg):
    config = configuration.ArtWorkConfig("BASE PLAYER CONFIGS")
    config.startTime = time.time()
    config.currentTime = time.time()
    config.doingReload = False
    config.brightnessOverride = None
    config.standAlone = True
    config.isRunning = True
    config.useDrawingPoints = False
    config.reloadConfig = False
    config.checkForConfigChanges = False
    main()


def producer(q,count):
  for i in range(5):
    print(f"Producing {i}")
    q.put((i, count))
    time.sleep(0.5)
  count +=1
  if count < 3 :
    print(f"\nNext round in 2s {count}")
    time.sleep(2)
    producer(q,count)
  else :
    q.put(None)           # Sentinel: tells consumer "we're done"

def consumer(q):
  while True:
    item = q.get()      # blocks until something is available
    if item is None:    # sentinel received
      break
    print(f"Consumed {item}")

if __name__ == "__main__":
  q = Queue()

  p1 = Process(target=producer, args=(q,0))
  p2 = Process(target=consumer, args=(q,))

  p3 = Process(target=launchPlayer, args=(q,))

  p1.count = 0

  p1.start()
  p2.start()
  p3.start()

  p1.join()
  p2.join()
  p3.join()