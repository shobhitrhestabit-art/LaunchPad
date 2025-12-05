


# api-investigation


API Investigation Report — Pagination, Headers, and Caching
# 1. Pagination Analysis
API Used:

https://dummyjson.com/products?limit=5&skip=10

# How Pagination Works

Pagination helps APIs return large datasets in small chunks so that:

The server does not overload

The client does not download too much data at once

Responses are fast and optimized

# Important Pagination Parameters



limit = 5  
skip = 10  


This means:

Skip first 10 products

Return 5 products starting from item 11

# Meaning in real world

Pagination is essential in:

Product listings

Social media feeds

Search results

Databases returning large datasets

# 2. HTTP Headers Analysis

During the lab we modified headers and observed changes.

## A. Without User-Agent

Command:

curl -v -H "User-Agent:" "https://dummyjson.com/products?limit=5"

# Observations

Server still returns data, because DummyJSON does not require a User-Agent.

But in real APIs:

Some APIs block unknown clients

User-Agent helps identify browser, OS, and client tool

Some security systems use User-Agent to detect bots

 Why removing User-Agent matters

Bots hide user-agent → security systems detect them
Browsers always send full user-agent → smoother API behavior

# B. Fake Authorization Header

Command:

curl -v -H "Authorization: Bearer faketoken123" https://dummyjson.com/products

# Observations

DummyJSON ignores the fake authorization header.

Response is still 200 OK.

No auth is required for this endpoint.

 Real API behavior:

APIs like GitHub, Stripe, Firebase → would reject with 401 Unauthorized

Authorization header is used to identify the user, role, and permissions.

## C. Request–Response Cycle Understanding

Your cURL -v output shows:

Request Headers

Host

Accept

User-Agent (or empty)

Authorization (when added)

Response Headers

Content-Type: application/json

Content-Length

Cache-Control

ETag (if available)

Server information

Date & time

These headers help browsers decide:

how to cache

how to present data

whether to re-request data

# 3. Caching + ETag Analysis

Caching helps avoid downloading the same data repeatedly.

A. Getting ETag

Command:

curl -I https://dummyjson.com/products/1


Headers included:

ETag: "some-value"
Cache-Control: public, max-age=xyz

# What is an ETag?

ETag = unique identifier for a specific version of data.

If data changes → ETag changes
If data is same → ETag remains same

B. Validating Cache Using ETag

Command:

curl -I -H "If-None-Match: \"etagvalue\"" https://dummyjson.com/products/1

Expected Response
304 Not Modified


Meaning:

Server knows your cached copy is fresh

No need to send full JSON again

Saves bandwidth and time

Why Caching Matters?
 Reduces network usage
 Speeds up page load
 Reduces server load
 Improves performance for repeated requests
# Summary
Topic	Summary
Pagination	Divides data into pages using limit + skip
Headers	Carry extra information: user-agent, authorization, content-type
ETag Caching	Prevents downloading unchanged data, gives 304 Not Modified

