#  Day 4 — SSL Setup with mkcert, Docker, NGINX & HTTPS

This document explains how I configured HTTPS locally using **NGINX**, **Docker**, and **mkcert**.  
It also includes screenshots and notes about browser certificate trust issues.

---

##  Project Structure


Day4/
│
├── app/ # Express backend + frontend
├── nginx/ # Reverse proxy config + certs
│ ├── nginx.conf
│ └── certs/
├── docker-compose.yml
└── screenshots


---

## 2. Installing mkcert

Install mkcert and its required utilities:

```bash
sudo apt install mkcert libnss3-tools
mkcert -install

```


## Generating ssl certificates

cd nginx/certs
mkcert mysite.local


## Mapping Local Domain 

127.0.0.1   mysite.local


## NGINX Configuration 

server {
    listen 443 ssl;
    server_name mysite.local;

    ssl_certificate /etc/nginx/certs/mysite.local.pem;
    ssl_certificate_key /etc/nginx/certs/mysite.local-key.pem;

    location / {
        proxy_pass http://app:3000;
    }
}

server {
    listen 80;
    return 301 https://$host$request_uri;
}


## Running via Docker compose

docker compose up --build 

##7 Browser intially showed "Not secure"

https://mysite.local

The browser displayed

Your connection is not private
NET::ERR_CERT_AUTHORITY_INVALID




## HTTPS Working Screenshot

![HTTPS Working](docs/https-working.png)


 ##solution 

 importingmkcert Root CA in firefox

##sceenshot

![Firefox CA Import](docs/firefox-ca-import.png)


