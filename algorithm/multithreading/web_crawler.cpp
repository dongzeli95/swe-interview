#include <mutex>
#include <unordered_set>
#include <queue>
#include <iostream>
#include <thread>

using namespace std;

class Solution {
public:
    mutex mtx;
    condition_variable cv;


    // Determine if we should terminate the crawling process.
    bool terminate = false;
    int workingCount = 0; // number of working thread


    // visited hashset and queue shared by all threads.
    unordered_set<string> visited;
    queue<string> q;


    string getHostName(string url) {
        size_t pos = url.find("://");


        // Extract the host name
        string host = url.substr(pos + 3);


        // Find the position of the "/" after the host name
        pos = host.find("/");


        // Extract the host name again
        return host.substr(0, pos);
    }


    void crawlWorkerDFS(int id, HtmlParser htmlParser, string curr) {
        Html html = htmlParser.fetch(curr);
        htmlParser.save(curr, html);
        vector<string> urls = htmlParser.parse(html);


        for (int i = 0; i < urls.size(); i++) {
            unique_lock<mutex> lock(mtx);
            if (visited.count(urls[i]) || getHostName(i) != getHostName(curr)) continue;
            visited.insert(urls[i]);
            lock.unlock();
            crawlWorkerDFS(id, htmlParser, urls[i]);
        }
    }

    void crawlWorker(int id, HtmlParser htmlParser) {
        while (true) {
            unique_lock<mutex> lock(mtx);
            // We only use worker with non-empty queue or the terminate condition is met.
            cv.wait(lock, [&]() {
                return q.size() || terminate;
                });


            // Terminate conditions: empty queue + no working worker.
            if (terminate) return;


            workingCount++;


            string curr = q.front();
            q.pop();


            lock.unlock();


            // Solution 1: Release lock here to save time.
            vector<string> urls = htmlParser.getUrls(curr);


            // Solution 2: Release lock here to save time.
            Html html = htmlParser.fetch(curr);
            // save
            thread fileIOThread([&] {
                htmlParser.save(curr, html);
                });


            // parse
            vector<string> urls = htmlParser.parse(html);


            lock.lock();
            for (string i : urls) {
                if (visited.count(i) || getHostName(i) != getHostName(curr)) continue;
                visited.insert(i);
                q.push(i);
            }


            workingCount--;
            if (workingCount == 0 && q.empty()) {
                terminate = true;
            }


            // Notify all other threads.
            cv.notify_all();
        }
    }


    std::thread t([]() {
        std::cout << "thread function\n";
        });
    std::cout << "main thread\n";
    t.join();


    vector<string> crawl(string startUrl, HtmlParser htmlParser) {
        q.push(startUrl);
        visited.insert(startUrl);


        int nThreads = thread::hardware_concurrency();
        vector<thread> threads;


        // Create a number of threads running the same function.
        for (int i = 0; i < nThreads; i++) {
            threads.emplace_back(&Solution::crawlWorker, this, i, htmlParser);
        }


        // Join and wait for all threads to finish.
        for (int i = 0; i < nThreads; i++) {
            threads[i].join();
        }


        return vector<string>(visited.begin(), visited.end());
    }
};