import time
from fastapi import Request, HTTPException

requests = {}

def rate_limiter(request: Request):
    ip = request.client.host
    now = time.time()

    if ip not in requests:
        requests[ip] = []

    requests[ip] = [t for t in requests[ip] if now - t < 60]

    if len(requests[ip]) > 100:
        raise HTTPException(429, "Too many requests")

    requests[ip].append(now)