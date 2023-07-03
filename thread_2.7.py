import threading
import time

class Box(object):
    lock = threading.RLock()

    def __init__(self):
        self.total_items = 0

    def execute(self, n):
        Box.lock.acquire()
        self.total_items += n
        Box.lock.release()

    def add(self):
        Box.lock.acquire()
        self.execute(1) # 此处再次调用了锁，如果使用lock，就会因为阻塞，而导致死锁。 由于是Rlock，可重入锁，并不会受影响。
        Box.lock.release()

    def remove(self):
        Box.lock.acquire()
        self.execute(-1)
        Box.lock.release()

## These two functions run n in separate
## threads and call the Box's methods
def adder(box, items):
    while items > 0:
        print("adding 1 item in the box")
        box.add()
        time.sleep(1)
        items -= 1

def remover(box, items):
    while items > 0:
        print("removing 1 item in the box")
        box.remove()
        time.sleep(1)
        items -= 1

## the main program build some
## threads and make sure it works
if __name__ == "__main__":
    items = 5
    print("putting %s items in the box " % items)
    box = Box()
    t1 = threading.Thread(target=adder, args=(box, items))
    t2 = threading.Thread(target=remover, args=(box, items)) # 此时，t2线程会因为锁的存在，而阻塞，直到t1释放锁时，t2才能继续执行。
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    #代码本质上是t1,t2争抢box内的资源，当其中一个线程获得锁时，另一个线程就会阻塞，直到释放锁，另一个线程才能继续执行。
    print("%s items still remain in the box " % box.total_items)