import multiprocessing
import os

import threading
from threading import *

import time
import random


class ReadersWriteLock():
    def __init__(self):
        self.cond_var = Condition()
        self.write_in_progress = False
        self.readers = 0

    def acquire_read_lock(self):
        self.cond_var.acquire()

        while self.write_in_progress is True:
            self.cond_var.wait()

        self.readers += 1

        self.cond_var.release()

    def release_read_lock(self):
        self.cond_var.acquire()

        self.readers -= 1
        if self.readers is 0:
            self.cond_var.notifyAll()

        self.cond_var.release()

    def acquire_write_lock(self):
        self.cond_var.acquire()

        while self.readers is not 0 or self.write_in_progress is True:
            self.cond_var.wait()
        self.write_in_progress = True

        self.cond_var.release()

    def release_write_lock(self):
        self.cond_var.acquire()

        self.write_in_progress = False
        self.cond_var.notifyAll()

        self.cond_var.release()

def writer_thread(lock):
    while 1:
        lock.acquire_write_lock()
        print("\n{0} writing at {1} and current readers = {2}".format(current_thread().getName(), time.time(),
                                                                      lock.readers), flush=True)
        write_for = random.randint(1, 5)
        time.sleep(write_for)
        print("\n{0} releasing at {1} and current readers = {2}".format(current_thread().getName(), time.time(),
                                                                        lock.readers),
              flush=True)
        lock.release_write_lock()
        time.sleep(1)


def reader_thread(lock):
    while 1:
        lock.acquire_read_lock()
        print("\n{0} reading at {1} and write in progress = {2}".format(current_thread().getName(), time.time(),
                                                                        lock.write_in_progress), flush=True)
        read_for = random.randint(1, 2)
        time.sleep(read_for)
        print("\n{0} releasing at {1} and write in progress = {2}".format(current_thread().getName(), time.time(),
                                                                          lock.write_in_progress), flush=True)
        lock.release_read_lock()
        time.sleep(1)
 
def print_cube(num):
    print("Cube: {}" .format(num * num * num))
 
 
def print_square(num):
    print("Square: {}" .format(num * num))

# // https://towardsdatascience.com/multithreading-vs-multiprocessing-in-python-3afeb73e105f#:~:text=The%20short%20answer%20is%3A,you%20have%20multiple%20cores%20available)

def worker1():
    print("ID of process running worker1: {}".format(os.getpid()))

def worker2():
    print("ID of process running worker2: {}".format(os.getpid()))

def test_multiprocessing():
    # printing main program process id 
    print("ID of main process: {}".format(os.getpid())) 
  
    # creating processes 
    p1 = multiprocessing.Process(target=worker1) 
    p2 = multiprocessing.Process(target=worker2) 
  
    # starting processes 
    p1.start() 
    p2.start() 
  
    # process IDs 
    print("ID of process p1: {}".format(p1.pid)) 
    print("ID of process p2: {}".format(p2.pid)) 
  
    # wait until processes are finished 
    p1.join() 
    p2.join() 
  
    # both processes finished 
    print("Both processes finished execution!") 
  
    # check if processes are alive 
    print("Process p1 is alive: {}".format(p1.is_alive())) 
    print("Process p2 is alive: {}".format(p2.is_alive())) 


    # Multithreading
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
 
    print("Done!")

# test on multithreading concurrency
shared_balance = 0

class Deposit(threading.Thread):
    def run(self):
        for _ in range(1000000):
            global shared_balance
            balance = shared_balance
            balance += 100
            shared_balance = balance

class Withdraw(threading.Thread):
    def run(self):
        for _ in range(1000000):
            global shared_balance
            balance = shared_balance
            balance -= 100
            shared_balance = balance

def test_multithread_balance():
    threads = [Deposit(), Withdraw()]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(shared_balance)

if __name__ == "__main__": 
    test_multithread_balance()

    lock = ReadersWriteLock()

    writer1 = Thread(target=writer_thread, args=(lock,), name="writer-1", daemon=True)
    writer2 = Thread(target=writer_thread, args=(lock,), name="writer-2", daemon=True)

    writer1.start()

    readers = list()
    for i in range(0, 3):
        readers.append(Thread(target=reader_thread, args=(lock,), name="reader-{0}".format(i + 1), daemon=True))

    for reader in readers:
        reader.start()

    writer2.start()

    time.sleep(15)