# Operating System

Obtaining high performance while maintaining control is central challenge in building an operating system.

## Limited Direct Execution

1. Boot time, kernel initializes trap table, CPU remembers its location for subsequent use. Kernel does so via a privileged instruction.
2. When running a process, the kernel allocating node on the process list, allocate memory before using a return-from-trap instruction to start the execution of the process.

## Switching between processes

Cooperative approach: Wait for system calls

Non-Cooperative approach: OS takes control by using timer interrupt and interrupt handler.

**Scheduler** decide whether to continue running the current running process or switch to a different one. (context switch)

## Scheduling

### Scheduling Metrics

T turnaround = T completion - T arrival

### Scheduling policies

1. FIFO suffers from long job that arrives early
2. SJF (Shortest Job First), this still suffer if jobs doesn't arrive at the same time, because we will be schedling longer job first.
3. STCF(Shortest time to completion first): terrible for response time since the jobs still have to wait to be started first run.

## Response time

T response = T firstrun - T arrival

## Round Robin

Instead of running jobs to completion, RR runs a job for a time slice. The shorter the timeslice, the better performance of RR is. However, it cannot be too short, the cost of context switching will dominate overall performance.

RR will perform pooly on turnaround time. Any fair policy will perform pooly on turnaround time.&#x20;

Trade offs: SJF, STCF optimizes turnaround time, but is bad for response time. RR optimizes response time but bad for turnaround time.

## Multi-level Feedback Queue

How can we design a scheduler that both minimizes response time for interactive jobs while also minimizing turnaround time without a priori knowledge of job length?

### Basic idea

1. If priority(A) > priority(B), A runs (B doesn't)
2. If priority(A) = priority(B), A\&B run in RR.

allotment is the amount of time a job can spend at a given priority level before the scheduler reduces its priority.

Rule 3: When a job enters the system, it is placed at the highest priority. (topmost queue)

Rule 4a: If a job uses up its allotment while running, its priority is reduced (moves down one queue)

Rule 4b: If a job gives up the CPU (by performing an I/O operation) before allotment is up, it stays at the same priority, allotment is reset.

Rule 5: After some time period S, move all the jobs in the system to the topmost queue. (used to solve starvation)

Rule 6: Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), its priority is reduced (moves down one queue). Use to prevent gaming the scheduler.

### Starvation with current MLFQ?

if there are too many interactive jobs in the system, they will combine to consume all CPU time, long-running jobs will starve.

A smart user can rewrite their program to game the scheduler.
