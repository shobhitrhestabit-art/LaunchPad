
# DAY 2 — Node CLI App + Concurrency + Large Data Processing

This project implements a high-performance Node.js CLI tool for analyzing large text files (200,000+ words).
It demonstrates asynchronous programming, concurrency, worker-based parallel processing, and performance benchmarking.




# Learning Outcome


Asynchronous file processing in Node.js

CLI tool development with arguments parsing

Concurrency using Promise.all() or worker_threads

Performance measurement for different concurrency levels

Large data handling & optimized text processing


# Tasks Completed

1. Generated a large corpus file (200,000+ words)

Using lorem generation & automated scripts.

2. Built CLI command
```bash
node wordstat.js --file corpus.txt --top 10 --minLen 5 --unique
```

3. CLI Output Includes

Total number of words

Unique word count

Longest word

Shortest word

Top N repeated words (configurable with --top)

![Wordstat Screenshot](https://raw.githubusercontent.com/shobhitrhestabit-art/Week1-Day2/main/wordstat.png)


4. Implemented Concurrency

File divided into chunks

Parallel processing using:

Promise.all() for async concurrency

OR worker_threads for true parallelism

5. Benchmarked 3 Concurrency Levels

1 worker

4 workers

8 workers

Results stored in:

```bash
logs/perf-summary.json
```

# lesson Learned

How to build real CLI apps in Node.js

How concurrency improves performance

Worker threads vs async concurrency

Efficient text parsing & large data processing

Using logs for runtime benchmarking