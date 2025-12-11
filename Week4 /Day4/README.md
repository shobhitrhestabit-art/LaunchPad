#  Day 4 — API Security, Validation, Rate Limiting & Hardening

Today’s focus was to secure the backend API using industry-standard middleware and protection layers.  
This includes sanitization, validation, rate limiting, CORS policies, Helmet headers, and attack prevention.

---

##  Objectives
- Protect APIs from common web attacks  
- Add robust validation (User + Product)  
- Implement global security middlewares  
- Apply rate limiting to prevent abuse  
- Inspect HTTP security headers  
- Create security test proofs (screenshots)

---

##  Topics Covered
- **Helmet** security hardening  
- **CORS** configuration  
- **Rate limiting** using `express-rate-limit`  
- **Payload size limits** (JSON + URL-encoded)  
- **NoSQL Injection Protection**  
- **XSS Mitigation**  
- **Parameter Pollution Prevention**  
- **Validation using Zod / Joi**  

---

##  Tasks Completed
###  Added global security middleware
Includes:
- Helmet security headers  
- CORS policy  
- JSON & URL-encoded body limits  
- NoSQL injection protection  
- XSS sanitization  
- Parameter pollution protection  

###  Implemented rate limiting
```
Limit: 100 requests
Window: 900 seconds
```

Headers observed:

- `RateLimit-Limit: 100`  
- `RateLimit-Remaining: 79`  
- `RateLimit-Reset: 799`  

###  Implemented validation middleware  
Created reusable validation schema for:
- User  
- Product  

###  Created manual security test cases  
Verified using:
- Browser  
- curl  
- Postman  

---

##  Folder Structure
```
src/
  middlewares/
    security.js     -> helmet, cors, rate-limit, sanitizers
    validate.js     -> request validation
  controllers/
  routes/
SECURITY-REPORT.md
```

---

##  API Tested
### `GET /api/health`
Response:
```json
{
  "status": "OK"
}
```

---

##  Screenshots (Proof of Security Work)

### **1️ Security Headers + Rate Limiting Response**
![Day4 Screenshot 1](![alt text](image-2.png))

---

### **2️curl header inspection showing Helmet + RateLimit**
![Day4 Screenshot 2](![alt text](image-1.png))

---

### ** Browser response showing health endpoint**
![Day4 Screenshot 3](![alt text](image.png))

---

##  Notes / Learnings
- Helmet adds **industry-standard security headers**, crucial for production APIs.  
- Rate limiting helps prevent DDoS, brute-force, and spam attacks.  
- Validation ensures **strict request bodies**, reducing business logic bugs.  
- CORS must be configured carefully; open `*` is acceptable only for internal/local APIs.  
- Payload size limits prevent large request attacks.  
- Sanitizers protect against **NoSQL injection**, **XSS**, and **parameter pollution**.

---


- 

---

##  Day 4 Completed Successfully  
This day solidifies the foundation of backend security.  
Your API is now **more secure, validated, rate-limited, and production-aligned.**

