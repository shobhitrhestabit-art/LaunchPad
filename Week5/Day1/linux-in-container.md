# Linux Inside Docker Container — Day 1 Exploration

This document contains the observations made by exploring a running Docker container for a Node.js application as part of Week-5 Day-1.

---

## 1. List Files (`ls -la`)

total 56
drwxr-xr-x 1 root root 4096 Dec 6 22:28 .
drwxr-xr-x 1 root root 4096 Dec 6 22:32 ..
-rw-rw-r-- 1 root root 116 Dec 6 17:18 Dockerfile
-rw-rw-r-- 1 root root 227 Dec 6 22:12 index.js
drwxr-xr-x 70 root root 4096 Dec 6 22:28 node_modules
-rw-r--r-- 1 root root 32545 Dec 6 22:28 package-lock.json
-rw-rw-r-- 1 root root 223 Dec 6 22:19 package.json



**Observations:**
- `/app` folder contains Dockerfile, index.js, package.json, and node_modules.
- These files were copied into the image during the Docker build.

---

## 2. Running Processes (`ps`)

PID TTY TIME CMD
14 pts/0 00:00:00 sh
26 pts/0 00:00:00 ps



**Observations:**
- `sh` is the shell opened via `docker exec`.
- The Node.js app runs as PID 1 (visible in `top` but not in basic `ps`).

---

## 3. Live CPU/Memory (`top`)

PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
1 root 20 0 992928 49532 40004 S 0.0 0.8 0:00.40 node
14 root 20 0 2584 1676 1568 S 0.0 0.0 0:00.03 sh
27 root 20 0 8652 4956 2832 R 0.0 0.1 0:00.00 top



**Observations:**
- The Node.js application is PID 1 → the main process of the container.
- System load is low.
- Only essential processes exist because containers run minimal OS environments.

---

## 4. Disk Usage (`df -h`)

Filesystem Size Used Avail Use% Mounted on
overlay 459G 2.5G 434G 1% /
tmpfs 64M 0 64M 0% /dev
shm 64M 0 64M 0% /dev/shm
/dev/vda1 459G 2.5G 434G 1% /etc/hosts


**Observations:**
- Container uses an **overlay filesystem**, common for Docker.
- `/etc/hosts` is mounted from the host.
- `tmpfs` is used for temporary in-memory storage.
- Disk usage is minimal because containers only store what is necessary.

---

## 5. Current User (`whoami`)


**Observations:**
- Containers run as **root** by default unless changed.
- This is common for Node.js official Docker images.

---

## 6. All System Users (`cat /etc/passwd`)

Common users found:

- root
- daemon
- bin
- sys
- mail
- www-data
- nobody
- node

**Observations:**
- These are standard Linux system users.
- `node` user exists because the Node.js image includes it.

---

## 7. Logs (`ls /var/log`)

alternatives.log
apt
btmp
dpkg.log
faillog
fontconfig.log
lastlog
wtmp



**Observations:**
- Debian-based container images include package manager logs (apt, dpkg).
- No large system logs because there are no system services running in the container.

---

## 8. Document Structure (`ls /`)

Expected directories (from your exploration):

- /bin  
- /etc  
- /lib  
- /usr  
- /tmp  
- /var  
- /dev  
- /root  
- /app → **Your Node.js project**

**Observations:**
- Container includes only essential Linux directories.
- `/app` is the working directory defined in the Dockerfile.

---

## 9. Summary & Key Learnings

- A Docker container acts like a **minimal Linux OS**.
- The Node application runs as **PID 1**, the main container process.
- Containers have isolated:
  - Filesystems  
  - Processes  
  - Users  
  - Memory  
  - Logs  
- Changes inside a container are **temporary** unless mounted via volumes.
- Docker's overlay filesystem enables lightweight and layered images.

---

**Day-1 task completed.**
