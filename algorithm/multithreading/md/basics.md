```cpp
#include <iostream>
#include <thread>
#include <condition_variable>

using namespace std;

// https://towardsdatascience.com/multithreading-vs-multiprocessing-in-python-3afeb73e105f#:~:text=The%20short%20answer%20is%3A,you%20have%20multiple%20cores%20available)

// Multithreading: good for I/O bound operations.
// Multiprocessing: good for CPU bound operations.

// function pointer.
void foo(int param) {
    cout << "function pointer: " << param << endl;
}

// lambda expression
auto f = [](int param) {
    cout << "function pointer: " << param << endl;
};

// Function object.
class fn_object_class {
    void operator() (int param) {
        cout << "function object: " << param << endl;
    }
};

class Base {
public:
  void foo(int param) {
    cout << "non-static: " << param << endl;
  }

  static void static_foo(int param) {
    cout << "static_foo: " << param << endl;
  }
};

// condition variables
// std::condition_variable is a synchronization primitive used with a std::mutex to block one 
// or more threads until another thread both modifies a shared variable(the condition) and notifies the std::condition_variable.

// The thread that intends to modify the shared variable must :

// Acquire a std::mutex(typically via std::lock_guard).
// Modify the shared variable while the lock is owned.
// Call notify_one or notify_all on the std::condition_variable(can be done after releasing the lock).
// Even if the shared variable is atomic, 
// it must be modified while owning the mutex to correctly publish the modification to the waiting thread.

// Any thread that intends to wait on a std::condition_variable must :

// Acquire a std::unique_lock<std::mutex> on the mutex used to protect the shared variable.
// Do one of the following :
// Check the condition, in case it was already updated and notified.
// Call wait, wait_for, or wait_until on the std::condition_variable(atomically releases the 
// mutex and suspends thread execution until the condition variable is notified, 
// a timeout expires, or a spurious wakeup occurs, then atomically acquires the mutex before returning).
// Check the condition and resume waiting if not satisfied.

// wait() - tells the current thread to wait till the condition variable is notified.
// wait_for() - tells the current thread to wait for some specific time duration. 
//              if notified early, the thread awakes.
// wait_until() - absolute time given instead of duration.
// notify_one() - notifies one of the waiting threads that shared resources is free to access.
//              thread selection is random.
// notify_all() - notifies all of the threads.

mutex mtx;
condition_variable cv;

bool data_ready = false;

void producer() {
  this_thread::sleep_for(chrono::seconds(2));
  // lock release 
  lock_guard<mutex> lock(mtx);
  // variable to avoid spurious wakeup 
  data_ready = true;
  // logging notification to console 
  cout << "Data Produced!" << endl;
  // notify consumer when done 
  cv.notify_one();
}

void consumer() {
  unique_lock<mutex> lock(mtx);
  cv.wait(lock, [] {
    return data_ready;
  });

  cout << "Data consumed!" << endl;
}

int main() {
    // // launching thread using function pointer.
    // thread thread_obj(foo, 2);

    // // launching thread using lambda expression.
    // thread thread_obj2(f, 2);

    // // launching thread using function object.
    // thread thread_obj3(fn_object_class(), 2);

    // // launching thread using non-static member function.
    // Base b;
    // thread thread_obj4(Base::foo, &b, 2);

    // // launching thread using static member function.
    // thread thread_obj5(&Base::foo, 2);

    // // Wait thread to finish.
    // thread_obj.join();

    thread consumer_t1(consumer);
    thread producer_t1(producer);

    consumer_t1.join();
    // producer_t1.join();

    return 0;
}```

```python
import multiprocessing
import os

import threading
 
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
    test_multithread_balance()```
