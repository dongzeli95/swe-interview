import time
import threading
from threading import *

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

class Value:
    def __init__(self, val, time):
        self.val = val
        self.time = time

class KVStoreLock:
    def __init__(self):
        self.m = {}
        self.timed_m = {}
        self.counter = 0
        self.lock = ReadersWriteLock()

    def get(self, k, time=None):
        self.lock.acquire_read_lock()
        try:
            if time is None:
                if k not in self.m:
                    raise ValueError("Key doesn't exist")
                return self.m[k]

            if k not in self.timed_m:
                raise ValueError("Key doesn't exist")

            val_list = self.timed_m[k]
            idx = self.search(val_list, time)
            if idx == -1:
                raise ValueError("Couldn't find key in time")

            return val_list[idx].val
        finally:
            self.lock.release_read_lock()

    def set(self, k, v):
        self.lock.acquire_write_lock()
        try:
            self.m[k] = v
            t = self.get_time()
            value = Value(v, t)
            if k not in self.timed_m:
                self.timed_m[k] = [value]
            else:
                self.timed_m[k].append(value)
        finally:
            self.lock.release_write_lock()

    def search(self, val_list, time):
        n = len(val_list)
        l, r = 0, n - 1

        res = -1
        while l <= r:
            m = l + (r - l) // 2
            if val_list[m].time == time:
                return m
            elif val_list[m].time < time:
                res = m
                l = m + 1
            else:
                r = m - 1

        return res

    def get_time(self):
        res = self.counter
        self.counter += 1
        return res

class KVStore:
    def __init__(self):
        self.m = {}
        self.timed_m = {}
        self.counter = 0

    def get(self, k, time=None):
        if time is None:
            if k not in self.m:
                raise ValueError("Key doesn't exist")
            return self.m[k]

        if k not in self.timed_m:
            raise ValueError("Key doesn't exist")

        val_list = self.timed_m[k]
        idx = self.search(val_list, time)
        if idx == -1:
            raise ValueError("Couldn't find key in time")

        return val_list[idx].val

    def set(self, k, v):
        self.m[k] = v
        t = self.get_time()
        value = Value(v, t)
        if k not in self.timed_m:
            self.timed_m[k] = [value]
        else:
            self.timed_m[k].append(value)

    def search(self, val_list, time):
        n = len(val_list)
        l, r = 0, n - 1

        res = -1
        while l <= r:
            m = l + (r - l) // 2
            if val_list[m].time == time:
                return m
            elif val_list[m].time < time:
                res = m
                l = m + 1
            else:
                r = m - 1

        return res

    def get_time(self):
        res = self.counter
        self.counter += 1
        return res

def set_values(store, key):
    for i in range(1000000):
        store.set(key, str(i))

def get_value(store, key):
    try:
        print(f"Value for {key}: {store.get(key)}")
    except ValueError as e:
        print(e)

def test_concurrent_write():
# Non-concurrent KVStore
    kv_store = KVStoreLock()

    # Creating threads for simultaneous writes
    thread2 = threading.Thread(target=kv_store.set, args=('k1', 'v1'))
    thread3 = threading.Thread(target=kv_store.set, args=('k1', 'v2'))
    thread1 = threading.Thread(target=kv_store.set, args=('k1', 'v3'))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    print('counter: ', str(kv_store.counter))
    # Reading the value after writes
    get_value(kv_store, 'k1')

if __name__ == "__main__": 
    # Testing the KVStore
    # kv_store = KVStore()
    # kv_store.set("k1", "v1") # 0
    # kv_store.set("k2", "v2") # 1
    # kv_store.set("k1", "v3") # 2

    # print(kv_store.get("k1")) # v3
    # print(kv_store.get("k1", 1)) # v1

    # kv_store.get_time() # 3
    # kv_store.get_time() # 4
    # kv_store.set("k1", "v4") # 5
    # print(kv_store.get("k1")) # v4
    # print(kv_store.get("k1", 0)) # v1
    # print(kv_store.get("k1", 1)) # v1
    # print(kv_store.get("k1", 2)) # v3
    # print(kv_store.get("k1", 3)) # v3
    # print(kv_store.get("k1", 4)) # v3
    # print(kv_store.get("k1", 5)) # v4
    # print(kv_store.get("k1", 6)) # v4
    # for i in range(50):
    test_concurrent_write()
