# Day 3 — NGINX Reverse Proxy + Load Balancing

## Overview
This exercise demonstrates how to use **NGINX inside Docker** as:

- A **reverse proxy**  
- A **load balancer**  
- A router for incoming API requests  

We deploy **two backend Node.js instances** and configure NGINX to balance traffic between them using **round-robin**.

All services are orchestrated using Docker Compose.

---

## Architecture

Client → NGINX → Backend Cluster → (backend1, backend2)


### Components:
- **backend1** — Node.js instance running on port 3000  
- **backend2** — Second Node.js instance (same code) also running on port 3000  
- **nginx** — Reverse proxy listening on port 8080  

NGINX forwards all `/api` requests to backend1 and backend2 **alternately**.

---

## How Load Balancing Works

NGINX upstream block:

upstream backend_cluster {
server backend1:3000;
server backend2:3000;
}


This defines a **cluster** of backend servers.

NGINX default load balancing method = **round-robin**, meaning:

1st request → backend1  
2nd request → backend2  
3rd request → backend1  
4th request → backend2  
…and so on.

---

## Routing

The following NGINX rule forwards all `/api` requests:

location /api {
proxy_pass http://backend_cluster;
}



So when the client calls:http://localhost:8080/api


NGINX forwards the request to backend1 or backend2.

---

## Running the Setup

Start all containers:
docker compose up -d



