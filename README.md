# Monpi – FastAPI Monitoring Middleware

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green)](https://fastapi.tiangolo.com)

**Monpi** is a dead simple, lightweight, plug‑and‑play monitoring middleware for FastAPI applications. It intercepts every request and response and send automated discord messages via webhooks for every server side exception and HTTP status code 500 and above , i.e , server erros
## Features

-  **Request/Response tracking** – stores URL, HTTP method, response time, status code
-  **Discord alerts** – sends detailed error notifications for 5xx status codes or unhandled exceptions
-  **In‑memory data store** – keeps a rolling history of the last N requests (configurable)
-  **Built‑in endpoints** – `/monitor/data` and `/monitor/health` to inspect collected metrics 
- **Zero‑overhead** – uses async middleware that doesn’t block your endpoints

## Installation
`pip install monpi`
```pip install monpi 
```
```

## Quick Start
```
````
````

```
from fastapi import FastAPI
from monpi.middleware import Monitor

app = FastAPI

monitor = Monitor(app = app,
                  alert=True,           //Optional If altert set to true you must provide discord webhooks url
                  discord_webhook = "your_discord_server_webhook_url",
                  save_limit = 1000,   //Save data of last 1000 request-response cycle, By default set to 100
                  )


```

After starting application you can for data in the following GET Endpoints

```
{BASE_URL}/monpi/data  //Returns Request ID, URL, Method, Response time

{BASE_URL}/monpi/health //Returns CPU and RAM usage percentage

```


