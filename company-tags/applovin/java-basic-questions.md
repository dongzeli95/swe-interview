# Java Basic Questions

## Difference between java versions?

Java has evolved significantly:

* Java 5 introduced generics and metadata annotations.
* Java 8 brought lambdas and the Stream API.
* Java 9 introduced modularity with the module system.
* Java 17 added sealed classes and pattern matching.

#### Garbage collection

1. **Serial Garbage Collection (Java 1.0 - Java 6):**
   * Single-threaded.
   * Suitable for single-threaded apps and small heap sizes.
   * Can cause noticeable pauses during GC.
2. **Parallel Garbage Collection (Java 5 - Java 9):**
   * Uses multiple threads.
   * Designed for throughput in multi-threaded apps.
   * Still has noticeable pauses during Full GC.
3. **CMS Garbage Collection (Java 5 - Java 8):**
   * Concurrent with the app for low latency.
   * Suitable for low-latency apps.
   * Can suffer from fragmentation issues.
4. **G1 Garbage Collection (Java 7 and later):**
   * Emphasizes predictability and low latency.
   * Divides heap into regions.
   * Adaptive for various app types and heap sizes.
5. **Z Garbage Collector (Java 11 and later):**
   * Very low-latency and large heap sizes.
   * Uses concurrent collection.
   * Versatile for different use cases.
6. **Shenandoah Garbage Collector (Java 12 and later):**
   * Ultra-low-latency, like ZGC.
   * Concurrent approach.
   * Suitable for large heaps and low-latency requirements.

## Why Python has GIL and other languages don't?

Global Interpreter Lock (GIL) is a mutex (lock) that allows only one thread to hold control of the python interpreter.

Python has the Global Interpreter Lock (GIL) to simplify memory management in its reference implementation, CPython. Other languages like Java and C++ have different concurrency models and memory management strategies that don't require a GIL. Removing the GIL from CPython would be complex and break backward compatibility, but Python provides alternatives like the multiprocessing module for parallelism.

## Multithreading

### What is multithreaded program?

A multithreaded program contains two or more parts that can run concurrently.&#x20;

### What are two ways Thread can be created?

1. Implementing Runnable interface.
2. Extending the Thread class.

| Runnable                                                                                                                                                                | Thread                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| <mark style="background-color:green;">Flexibility: As you can implement multiple interfaces in Java, it allows your class to extend other classes.</mark>               | <mark style="background-color:red;">Limited ability to use other classes or interfaces, leading to less flexible design.</mark> |
| <mark style="background-color:green;">Resource sharing: multiple threads can share the same Runnable object, which can be useful for sharing data among threads.</mark> | <mark style="background-color:green;">You can create and start thread without creating additional Thread object.</mark>         |

<pre class="language-java"><code class="lang-java"><strong>// Runnable
</strong><strong>class MyRunnable implements Runnable {
</strong>    public void run() {
        // Thread behavior here
    }
}
Thread thread = new Thread(new MyRunnable());
thread.start();

// Thread
class MyThread extends Thread {
    public void run() {
        // Thread behavior here
    }
}
MyThread thread = new MyThread();
thread.start();
</code></pre>
