import time
import threading
from threading import *
import json
from glob import glob

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

    def __repr__(self):
        return "Value(val={}, time={})".format(self.val, self.time)

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

def set_values(store, key):
    for i in range(1000000):
        store.set(key, str(i))

def get_value(store, key):
    try:
        print(f"Value for {key}: {store.get(key)}")
    except ValueError as e:
        print(e)


class KVStoreLockWithDiskFlush:
    def __init__(self, filename_template="store_{}.json", ttl_seconds = 2):
        self.m = {}
        self.timed_m = {}
        self.counter = 0
        self.lock = ReadersWriteLock()

        self.filename_template = filename_template
        self.ttl_seconds = ttl_seconds

        self.files = []
        self.last_flush_time = time.time()
        self.start_flushing_thread()

    def get_filename(self, timestamp):
        return self.filename_template.format(timestamp)

    def flush_to_disk(self):
        self.lock.acquire_write_lock()

        flushing_time = time.time()
        self.last_flush_time = flushing_time

        try:
            cutoff_timestamp = flushing_time - self.ttl_seconds
            old_data_timed_map = {}

            for key, val_list in self.timed_m.items():
                old_val_list = [val for val in val_list if val.time < cutoff_timestamp]
                if old_val_list:
                    old_data_timed_map[key] = old_val_list

            data_to_dump = {
                'timed_map': {k: [vars(val) for val in v] for k, v in old_data_timed_map.items()}
            }

            # Create a filename that includes the cutoff timestamp
            filename = self.get_filename(cutoff_timestamp)
            self.files.append(filename)
            with open(filename, 'w') as f:
                json.dump(data_to_dump, f)

            for key, old_val_list in old_data_timed_map.items():
                self.timed_m[key] = [val for val in self.timed_m[key] if val.time >= cutoff_timestamp]
        finally:
            self.lock.release_write_lock()

    def load_from_disk(self, key, time=None):
        # Step 1: Gather all JSON files in the current directory
        json_files = self.files

        # Step 2 & 3: Binary search for the appropriate file based on the timestamp
        file_to_read = None
        if time is not None:
            left, right = 0, len(json_files) - 1
            while left <= right:
                mid = left + (right - left) // 2
                mid_time = self.extract_timestamp_from_filename(json_files[mid])
                
                if mid_time <= time:
                    file_to_read = json_files[mid]
                    left = mid + 1
                else:
                    right = mid - 1
        else:
            # If time is None, just use the last file (latest)
            file_to_read = json_files[-1] if json_files else None

        # Step 4: Load and search data
        if file_to_read:
            try:
                with open(file_to_read, 'r') as f:
                    data = json.load(f)

                    if time is not None and key in data['timed_map']:
                        val_list = [Value(**val) for val in data['timed_map'][key]]
                        idx = self.search(val_list, time)
                        if idx != -1:
                            return val_list[idx].val
            except FileNotFoundError:
                pass

        return None

    def extract_timestamp_from_filename(self, filename):
        # Remove the preceding 'store_' and the '.json' extension to extract the timestamp
        timestamp_str = filename[len('store_'):-len('.json')]
        try:
            return int(timestamp_str)
        except ValueError:
            # Handle cases where the timestamp is not a valid integer
            raise ValueError("Invalid filename format: Cannot parse timestamp from '{}'".format(filename))

    def get(self, k, time=None):
        self.lock.acquire_read_lock()
        try:
            res = None
            if time is None:
                if k in self.m:
                    res = self.m[k]
            else:
                if k in self.timed_m:
                    val_list = self.timed_m[k]
                    idx = self.search(val_list, time)
                    if idx != -1:
                        res = val_list[idx].val

            if res is None:
                res = self.load_from_disk(k, time)
            return res
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
        # print("search val list: ", str(val_list))
        for i in range(len(val_list)):
            print(str(val_list[i]))
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
        return time.time()

    def should_flush(self):
        return time.time() - self.last_flush_time > self.ttl_seconds
    
    def start_flushing_thread(self):
        def flush_periodically():
            while True:
                if self.should_flush():
                    self.flush_to_disk()

        threading.Thread(target=flush_periodically, daemon=True).start()

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
    kv_store = KVStoreLockWithDiskFlush()

    # Creating threads for simultaneous writes
    thread2 = threading.Thread(target=kv_store.set, args=('k1', 'v1'))
    thread3 = threading.Thread(target=kv_store.set, args=('k1', 'v2'))
    thread1 = threading.Thread(target=kv_store.set, args=('k1', 'v3'))
    thread4 = threading.Thread(target=kv_store.set, args=('k1', 'v4'))
    thread5 = threading.Thread(target=kv_store.set, args=('k1', 'v5'))

    thread1.start()
    time.sleep(2)
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()


    print('counter: ', str(kv_store.counter))
    # Reading the value after writes
    get_value(kv_store, 'k1')

def generate_dummy_data(kv_store, num_entries, time_interval):
    """
    Generates dummy data and triggers flush_to_disk method.

    :param kv_store: An instance of KVStoreLockWithDiskFlush
    :param num_entries: Number of entries to create
    :param time_interval: Time interval (in seconds) between entries
    """
    for i in range(num_entries):
        key = f"key_{i}"
        value = f"value_{i}"
        kv_store.set(key, value)

        # Simulate time passage
        time.sleep(time_interval)

        # Optionally trigger flush based on some condition
        if i % 10 == 0:  # Example condition, adjust as needed
            kv_store.flush_to_disk()


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
