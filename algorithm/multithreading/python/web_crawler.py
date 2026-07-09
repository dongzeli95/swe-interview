"""
LeetCode 1242: Web Crawler Multithreaded

Mirrors algorithm/multithreading/cpp/web_crawler.cpp 1-to-1.

Approaches (single Solution class, matching the C++ source):
  - crawlWorkerDFS: Recursive DFS worker that fetches, saves, and parses each
    URL, recursing into same-host children. Time: O(V + E) over the reachable
    same-host graph. Space: O(V) for the visited set plus recursion depth.
  - crawlWorker: BFS-style worker driven by a shared queue and condition
    variable. Multiple worker threads pop URLs, fetch/parse in parallel while
    holding the lock only around queue/visited mutations. Time: O(V + E)
    across all workers. Space: O(V) for the visited set and queue.

Both workers share a single Solution instance's state (visited set, queue,
mutex, condition variable, workingCount, terminate flag). The public entry
point `crawl` spawns `os.cpu_count()` worker threads running `crawlWorker`
and returns the visited set once the workers converge on the termination
condition (queue empty and no worker actively processing).

Note: HtmlParser / Html are external types provided by the judge; they are
referenced here as `Any` for type-hint purposes only, matching the C++
skeleton which also assumes them as external.
"""

from __future__ import annotations

import os
import threading
from collections import deque
from typing import Any, List, Set


class Solution:
    def __init__(self) -> None:
        self.mtx = threading.Lock()
        self.cv = threading.Condition(self.mtx)

        # Determine if we should terminate the crawling process.
        self.terminate: bool = False
        self.workingCount: int = 0  # number of working threads

        # visited hashset and queue shared by all threads.
        self.visited: Set[str] = set()
        self.q: deque[str] = deque()

    def getHostName(self, url: str) -> str:
        pos = url.find("://")

        # Extract the host name
        host = url[pos + 3:]

        # Find the position of the "/" after the host name
        slash = host.find("/")
        if slash == -1:
            return host

        # Extract the host name again
        return host[:slash]

    def crawlWorkerDFS(self, id: int, htmlParser: Any, curr: str) -> None:
        html = htmlParser.fetch(curr)
        htmlParser.save(curr, html)
        urls: List[str] = htmlParser.parse(html)

        for i in range(len(urls)):
            with self.mtx:
                if urls[i] in self.visited or self.getHostName(urls[i]) != self.getHostName(curr):
                    continue
                self.visited.add(urls[i])
            self.crawlWorkerDFS(id, htmlParser, urls[i])

    def crawlWorker(self, id: int, htmlParser: Any) -> None:
        while True:
            with self.cv:
                # We only use worker with non-empty queue or the terminate condition is met.
                self.cv.wait_for(lambda: len(self.q) > 0 or self.terminate)

                # Terminate conditions: empty queue + no working worker.
                if self.terminate:
                    return

                self.workingCount += 1

                curr = self.q.popleft()

            # Solution 1: Release lock here to save time.
            urls: List[str] = htmlParser.getUrls(curr)

            # Solution 2: Release lock here to save time.
            html = htmlParser.fetch(curr)

            # save (file I/O in a background thread)
            file_io_thread = threading.Thread(target=lambda: htmlParser.save(curr, html))
            file_io_thread.start()

            # parse
            urls = htmlParser.parse(html)

            with self.cv:
                for i in urls:
                    if i in self.visited or self.getHostName(i) != self.getHostName(curr):
                        continue
                    self.visited.add(i)
                    self.q.append(i)

                self.workingCount -= 1
                if self.workingCount == 0 and not self.q:
                    self.terminate = True

                # Notify all other threads.
                self.cv.notify_all()

            file_io_thread.join()

    def crawl(self, startUrl: str, htmlParser: Any) -> List[str]:
        self.q.append(startUrl)
        self.visited.add(startUrl)

        nThreads = os.cpu_count() or 1
        threads: List[threading.Thread] = []

        # Create a number of threads running the same function.
        for i in range(nThreads):
            t = threading.Thread(target=self.crawlWorker, args=(i, htmlParser))
            threads.append(t)
            t.start()

        # Join and wait for all threads to finish.
        for t in threads:
            t.join()

        return list(self.visited)
