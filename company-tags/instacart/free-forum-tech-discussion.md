# Free forum tech discussion

#### Explain the meaning of multithreading.

The thread is an independent part or unit of a process (or an application) that is being executed. Whenever multiple threads execute in a process at the same time, we call this "multithreading". You can think of it as a way for an application to multitask.

| S.NO | Process                                                                             | Thread                                                                                                                                                                       |
| ---- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.   | Process means any program is in execution.                                          | Thread means a segment of a process.                                                                                                                                         |
| 2.   | The process takes more time to terminate.                                           | The thread takes less time to terminate.                                                                                                                                     |
| 3.   | It takes more time for creation.                                                    | It takes less time for creation.                                                                                                                                             |
| 4.   | It also takes more time for context switching.                                      | It takes less time for context switching.                                                                                                                                    |
| 5.   | The process is less efficient in terms of communication.                            | Thread is more efficient in terms of communication.                                                                                                                          |
| 6.   | Multiprogramming holds the concepts of multi-process.                               | We don’t need multi programs in action for multiple threads because a single process consists of multiple threads.                                                           |
| 7.   | The process is isolated.                                                            | Threads share memory.                                                                                                                                                        |
| 8.   | The process is called the heavyweight process.                                      | A Thread is lightweight as each thread in a process shares code, data, and resources.                                                                                        |
| 9.   | Process switching uses an interface in an operating system.                         | Thread switching does not require calling an operating system and causes an interrupt to the kernel.                                                                         |
| 10.  | If one process is blocked then it will not affect the execution of other processes  | If a user-level thread is blocked, then all other user-level threads are blocked.                                                                                            |
| 11.  | The process has its own Process Control Block, Stack, and Address Space.            | Thread has Parents’ PCB, its own Thread Control Block, and Stack and common Address space.                                                                                   |
| 12.  | Changes to the parent process do not affect child processes.                        | Since all threads of the same process share address space and other resources so any changes to the main thread may affect the behavior of the other threads of the process. |
| 13.  | A system call is involved in it.                                                    | No system call is involved, it is created using APIs.                                                                                                                        |
| 14.  | The process does not share data with each other.                                    | Threads share data with each other.                                                                                                                                          |

#### Golang (Go)

**Strengths:**

* Concurrency support: Go's goroutines and channels make concurrent programming more accessible and efficient.
* Simplicity and readability: Go has a clean syntax with minimalistic features, which makes it easy to learn and read.
* Fast compilation: Go compiles directly to machine code, offering fast execution.

**Limitations:**

* Lack of generics (until recently): Traditional Go did not support generics, which limited the ability to create flexible data structures and functions. However, this was addressed in recent updates.
* Simplicity as a double-edged sword: The simplicity of Go can be limiting for some complex applications where advanced language features (like those found in C++ or Java) are beneficial.
* Garbage collection: While it simplifies memory management, Go's garbage collector can introduce pauses and affect performance in high-load scenarios.

#### C++

**Strengths:**

* Performance: As a lower-level language, C++ offers high performance and fine control over system resources.
* Object-Oriented Programming: C++ supports advanced object-oriented concepts, making it suitable for large, complex software systems.
* Versatility: It's used in various domains, from game development to system programming.

**Limitations:**

* Complexity: C++ has a steep learning curve due to its complexity and vast feature set.
* Memory Management: Manual memory management can lead to issues like memory leaks and is generally more challenging to manage than in garbage-collected languages.
* Lengthier code: Compared to languages like Go, C++ can require more code to accomplish the same task, impacting development time and maintainability.
*

### **What is Mutex?** <a href="#what-is-mutex" id="what-is-mutex"></a>

A Mutex or Mutual Exclusion Object is used to allow only one of the processes access to the resource at a time. The Mutex object allows all processes to use the same resource, but the resource is accessed by one process at a time. Mutex uses a lock-based approach to handle critical section issues.

Each time a process requests a resource from the system, the system creates a mutex object with a unique name or ID. So whenever a process wants to use that resource, it acquires a lock on the object. After locking, the process uses the resource and eventually releases the mutex object. Other processes can then create and use mutex objects in the same way.

### **Advantages of Mutex** <a href="#advantages-of-mutex" id="advantages-of-mutex"></a>

* Mutex is to create a barrier that prevents two different threads from accessing a resource simultaneously. This prevents resources from being unavailable when another thread needs them.
* Mutex is that it can help with code reliability. Resources accessed by a thread can become unavailable if the CPU’s memory management fails. By preventing access to a resource at this time, the system can recover from any errors that cause a failure in memory management and still have the resource available, and Mutex helps here.

### **Disadvantages of Mutex** <a href="#disadvantages-of-mutex" id="disadvantages-of-mutex"></a>

* It cannot be locked or unlocked by any context other than the context that acquired it.
* Typical implementations can result in busy wait states that waste CPU time.
* If one thread acquires the lock, goes to sleep, or becomes preemptive, the other thread may get stuck further. This can lead to hunger.
* In the critical section, he should only allow one thread at a time.

&#x20;

### **What is a semaphore?** <a href="#what-is-a-semaphore" id="what-is-a-semaphore"></a>

A semaphore is an integer variable S that is initialized with the number of resources present in the system and used for process synchronization. Change the value of S using two functions: wait() and signal(). These two functions are used to change the value of a semaphore, but they allow only one process to change the value at any given time. Two processes cannot change the value of a semaphore at the same time. Semaphores have two categories: **counting semaphores** and **binary semaphores.**

### **Advantages of semaphore** <a href="#advantages-of-semaphore" id="advantages-of-semaphore"></a>

* **Efficient Allocation:** Semaphores allow you to allocate system resources more efficiently. This means that memory can be used more effectively.
* **Controlling multiple processes:** Semaphores allow you to control multiple processes. This means you can allocate memory to specific tasks as needed.
* **Improved performance:** Semaphore-based memory management improves performance and improves system responsiveness.



Overloading happens when you keep the same method name but change the number or type of parameters. Overriding occurs when you keep the same method name and signature but change the implementation. Also, you can overload private and static methods, but you cannot override them.

### Event Loop

The event loop in JavaScript enables asynchronous programming. With JS, every operation takes place on a single thread, but through smart data structures, we can create the illusion of multi-threading. With the Event Loop, any async work is handled by a queue and listener.

Therefore, when an async function (or an I/O) needs to be executed, the main thread relays it to another thread, allowing v8 (Javascript engine) to continue processing or running its code. In the event loop, there are different phases, like pending callbacks, closing callbacks, timers, idle or preparing, polling, and checking, with different FIFO (First-In-First-Out) queues.



### Dependency Injection

The Dependency Injection (DI) pattern is a design pattern for implementing the Inversion of Control (IoC). Dependent objects can be created outside of classes and made available to classes in different ways.

* Client Class: A client class (dependent class) is one that depends on the service class.
* Service Class: Service (dependency) classes provide services to client classes.
* Injector Class: This class injects the objects from the service class into the client class.



### Observer Pattern

If several objects are tied together in one-to-many relationships, the observer pattern is used. Every time one object is modified, then all of its dependent objects are automatically notified and updated. It falls under the behavioural pattern category. It describes the coupling between the objects and the observer and provides support for broadcast-type communication.



### Normalization vs Denormalization

| Normalization                                                                                                                           | Denormalization                                                                                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Normalization involves removing redundant data (multiple copies of data) from a database and storing consistent, non-redundant data.    | It involves combining data from multiple tables into a single so that it can be queried quickly.                                                     |
| It primarily focuses on clearing out unused data and reducing duplicate data and inconsistencies from a database.                       | On the other hand, denormalization aims to achieve faster query execution by adding data redundancy.                                                 |
| During normalization, tables are reduced in number due to the reduction of data in the database.                                        | Denormalization, on the other hand, involves integrating data into the same database and therefore the number of tables to store the data increases. |
| Data integrity is maintained by normalization. A change to the data in the table will not impact its relationship with the other table. | Data integrity is not maintained by denormalization.                                                                                                 |
| It optimizes the use of disk space.                                                                                                     | It does not optimize disk space.                                                                                                                     |



### Promise and its state

* **Pending:** In its initial state, neither fulfilled nor rejected.
* **Fulfilled:** Indicating that the operation was successful.
* **Rejected:** Indicating that the operation failed.

\


### GET vs POST

| GET                                                                                                                                                                    | POST                                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| This method is used to request data from a certain resource (via some API URL).                                                                                        | This method is used to send or write data to be processed to a specific resource (via some API URL).                          |
| If you use the GET method to send data, the data is added to the URL, and a URL can be up to 2048 characters in length. Therefore, it has restrictions on data length. | It does not impose such limitations.                                                                                          |
| In comparison to POST, GET is less secure since data is sent as part of the URL. Passwords and other sensitive information should never be sent using GET.             | It is a little safer to use POST than GET because the parameters are not saved in the browser history or the web server logs. |
| Everyone can see the data in the URL.                                                                                                                                  | There is no data displayed in the URL.                                                                                        |



### MEAN

MEAN stands for MongoDB, ExpressJS, AngularJS, and Node.js. It is a collection of JavaScript-based technologies for developing web applications. Despite being a stack of different technologies, all of them are based on the JavaScript language. It is an ideal solution for building dynamic websites and applications as it is a very user-friendly stack. With this free and open-source stack, you can quickly and easily build web-based prototypes.

\


### MVC vs MVP

| MVC                                                                                                                                                                                                             | MVP                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MVC suggests splitting the code into three components. As soon as the developer creates a class or file for an application, he or she must categorize it into one of three layers: Model, View, and Controller. | This is an architectural pattern that helps compensate for some of the shortcomings of MVC. It is composed of three components i.e., Model, View, and Presenter.                                                            |
| The controller serves as a bridge between the view and model layers and therefore provides the application's user interface. As soon as the Model changes, the Controller updates the View.                     | The presenter pulls data from the model and applies the UI  (user interface) logic to determine what to show. In response to the user's input notification, it manages the state of the View and takes appropriate actions. |
| Controllers and views have a many-to-one relationship since one Controller can select different Views depending on the operation required.                                                                      | Presenter and View have a one-to-one relationship since the Presenter class manages only one View at a time.                                                                                                                |
| Support for unit testing is limited.                                                                                                                                                                            | The unit testing process is highly supported.                                                                                                                                                                               |



### Event bubbling vs event capturing

The propagation of events inside the DOM (Document Object Model) is known as 'Event Flow' in JavaScript. The event flow defines the order or sequence in which a particular web page receives an event. Accordingly, event flow (propagation) in JS is dependent on the following aspects:

* **Event Bubbling:** With Event Bubbling, the event is captured and handled first by the innermost element, and then propagates to the outermost element. Events propagate up the DOM tree from child elements until the topmost element is handled.
* **Event Capturing:** With Event Capturing, the event is captured and handled first by the outermost element, and then propagates to the innermost element. Event cycles propagate starting with the wrapper elements and ending with the target elements that initiated the event cycle.

The following diagram will help you to understand the event propagation life cycle.

### Temporal deadzone

Before ES6, variable declarations were only possible using var. With ES6, we got let and const. Both let and const declarations are block-scoped, i.e., they can only be accessed within the " { } " surrounding them. On the other hand, var doesn't have such a restriction. Unlike var, which can be accessed before its declaration, you cannot access the let or const variables until they are initialized with some value. Temporal Dead Zone is the time from the beginning of the execution of a block in which let or const variables are declared until these variables are initialized. If anyone tries to access those variables during that zone, Javascript will always throw a reference error as given below.

```plaintext
console.log(varNumber); // undefined
console.log(letNumber); // Throws the reference error letNumber is not defined
var varNumber = 3;
let letNumber = 4;
```

Both let and const variables are in the TDZ from the moment their enclosing scope starts to the moment they are declared.



### Arrow function not used in ES6?

One of the most popular features of ES6 is the "arrow functions" (also known as "fat arrow functions"). Arrow functions are a new way to write concise functions. Arrow functions offer a compact alternative to traditional function expressions, but they have limitations and cannot be used in every case.

The following is an ES5 function:

```plaintext
function timesTwo(params) {
        return params * 2
     }
timesTwo(5);  // 10
```

The same function can also be expressed as an arrow function in ES6 as follows:

```plaintext
var timesTwo = params => params * 2
timesTwo(5);  // 10
```



###
