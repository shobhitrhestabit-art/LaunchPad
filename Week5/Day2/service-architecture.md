# Service Architecture — Docker Compose Multi-Container App (Day 2)

This document explains the architecture of a multi-container application that includes:

- **React Client** (Frontend)
- **Node.js Server** (Backend API)
- **MongoDB Database**
- **Docker Compose** (Orchestration)

All three services run together using a single command:


---

## 1. Architecture Overview

The system consists of three separate containers, each with its own responsibility:

| Service | Role |
|--------|------|
| **client** | React frontend served on port 3000 |
| **server** | Express.js backend running on port 5000 |
| **mongo** | MongoDB database storing the application data |

Docker Compose orchestrates these services and ensures they communicate correctly.

---

## 2. Container Networking

Docker Compose creates an **automatic private network** for all services.

This allows containers to communicate using **service names** instead of IP addresses.

### Service-to-Service Communication:
- Node server connects to MongoDB using:mongodb://mongo:27017/mydb


- Client connects to backend using:http://server:5000


### Benefits:
- No need to manually configure IPs  
- All containers can “see” each other  
- Automatic DNS resolution inside Compose network  

---

## 3. Volumes & Persistent Storage

MongoDB requires persistent storage so that data is not lost when the container restarts.

In the Compose file:

```yaml
volumes:
- mongo_data:/data/db

