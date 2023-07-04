# -*- coding: utf-8 -*-

"""Using a Semaphore to synchronize threads"""
import threading
import time
import random

# The optional argument gives the initial value for the internal
# counter;
# it defaults to 1.
# If the value given is less than 0, ValueError is raised.
semaphore = threading.Semaphore(0)

def consumer():
        print("consumer is waiting.")
        # Acquire a semaphore
        semaphore.acquire() #第一次获取时会被阻塞， semaphore.acquire()并不会锁住某些值，他只是会在判定semaphore小于等用0时，阻塞线程，直到有另一个线程release，semaphore的值变为1时，才会继续执行。
        # The consumer have access to the shared resource
        print("Consumer notify : consumed item number %s " % item)

def producer():
        global item
        time.sleep(10)
        # create a random item
        item = random.randint(0, 1000)
        print("producer notify : produced item number %s" % item)
         # Release a semaphore, incrementing the internal counter by one.
        # When it is zero on entry and another thread is waiting for it
        # to become larger than zero again, wake up that thread.
        semaphore.release() # 程序会先需要release一次，才能把semaphore的值变为1，然后consumer的acquire才能继续执行。所以程序第一次运行时一定是producer先执行完毕，然后consumer才能执行。

if __name__ == '__main__':
        for i in range (0,5) :
                t1 = threading.Thread(target=producer)
                t2 = threading.Thread(target=consumer)
                t1.start()
                t2.start()
                t1.join()
                t2.join()
        print("program terminated")