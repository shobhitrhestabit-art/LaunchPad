
# System Reverse Engineering + Node & Terminal Mastering

This project contains all the work completed for **Day-1**, focused on understanding the system, mastering terminal commands, exploring Node.js internals, analysing environment variables, and performing performance benchmarking using Streams & Buffers.

All system-level details were collected **using only the terminal**, without any GUI tools.



## Authors


Shobhit Raj
Date: 10 Nov 2025

- [Link](https://github.com/shobhitrhestabit-art)


## Features

- System Introspection (OS, CPU, Memory, User, Uptime, Node Path)
- Terminal-only environment analysis  
- NVM installation and Node version switching  
- PATH & environment variable investigation  
- Stream vs Buffer file-reading benchmark  
- Performance logs generated in JSON  
- Clean documentation via `system-report.md`  


## Tech Stack

**Client:** React, Redux, TailwindCSS

**Server:** Node, Express


## Deployment

To deploy this project run

```bash
  npm run deploy
```
OS Version

```bash
  uname -a
```


Shell Type

```bash
  echo $SHELL
```


Node Binary Path

```bash
  npm root -g
```

Path entries containing node/npm

```bash
  echo $PATH | tr ':' '\n' | grep -i 'node\|npm'
```
## STREAM vs BUFFER Performance


This project includes a benchmarking exercise comparing **Buffer (`fs.readFile`)** and **Stream (`fs.createReadStream`)** methods in Node.js for reading a large 50MB+ file.


Buffer Method (`fs.readFile`)
Reads the entire file into memory at once.

- Faster execution  
- Very high RAM usage  
- Can crash on very large files  

```bash
node --expose-gc introspect.js ./read-buffer.js logs/day1-perf-buffer.json
```
Stream Method (`fs.createReadStream`)

The **Stream** approach reads the file **chunk by chunk** instead of loading everything into memory at once.  
This makes it highly efficient for working with large files (50MB+).

```bash
node --expose-gc introspect.js ./read-stream.js logs/day1-perf-stream.json

```

Conclusion

Buffer is faster but consumes a lot of memory.

Stream is slower but extremely memory-efficient.

For large files, Stream should always be used.
