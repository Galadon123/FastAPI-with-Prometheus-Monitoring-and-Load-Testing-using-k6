from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Gauge, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

app = FastAPI()

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total request count')
POST_REQUEST_COUNT = Counter('post_request_count', 'Total POST request count')  # New POST request counter
RANDOM_GAUGE = Gauge('random_gauge', 'A random gauge value')

@app.get("/")
async def root():
    REQUEST_COUNT.inc()  # Increment the GET request counter
    RANDOM_GAUGE.set(time.time() % 60)  # Set gauge to current seconds of the minute
    return {"message": "Hello World"}

@app.post("/submit")
async def submit(data: dict):
    """
    POST endpoint that accepts a JSON payload and returns it back.
    """
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")
    POST_REQUEST_COUNT.inc()  # Increment the POST request counter
    return {"received_data": data}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
