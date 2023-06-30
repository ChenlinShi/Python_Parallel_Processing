import threading
import time

def function(i):
    print ("function called by thread %i\n" % i)
    time.sleep(5)  # Add some delay.
    return

threads = []

# Start all threads.
for i in range(5):
    t = threading.Thread(target=function , args=(i, )) # create a thread for each i.
    threads.append(t) # add each thread to the list.
    t.start() # start the thread. 

# Wait for all threads to complete.
for t in threads:
    t.join()  # make sure each thread has finished before moving on.
    


