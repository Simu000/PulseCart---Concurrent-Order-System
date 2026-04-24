from flask import Flask, render_template, redirect, url_for, request
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# -----------------------------
# Shared Buffer using Semaphore
# -----------------------------
BUFFER_SIZE = 5
buffer = []

empty = threading.Semaphore(BUFFER_SIZE)   # free slots
full = threading.Semaphore(0)              # filled slots
mutex = threading.Lock()                   # critical section lock

# -----------------------------
# Global Data
# -----------------------------
stock = 3
logs = []
mode = "CONSISTENCY"
order_id = 101


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template(
        "index.html",
        stock=stock,
        qsize=len(buffer),
        mode=mode,
        logs=logs
    )


# -----------------------------
# Producer 
# -----------------------------
async def producer_task():
    global order_id

    await asyncio.sleep(0.2)  # simulate delay

    if not empty.acquire(blocking=False):
    	logs.append("Queue Full: Customer must wait")
    	return

    with mutex:
        buffer.append(order_id)
        logs.append(f"Customer Order {order_id} added")
        order_id += 1

    full.release()


# -----------------------------
# Add Order 
# -----------------------------
@app.route("/add", methods=["GET", "POST"])
def add():
    asyncio.run(producer_task())

    # If called from test script (POST)
    if request.method == "POST":
        return {"status": "ok"}, 200

    # If called from browser
    return redirect(url_for("home"))


# -----------------------------
# Consumer
# -----------------------------
def consume_one():
    global stock

    if not full.acquire(blocking=False):
        logs.append("Queue Empty: No orders to process")
        return

    with mutex:
        oid = buffer.pop(0)

    empty.release()

    with mutex:
        if stock > 0:
            stock -= 1
            logs.append(f"Order {oid}: SUCCESS")
        else:
            if mode == "CONSISTENCY":
                logs.append(f"Order {oid}: REJECTED (Out of Stock)")
            else:
                logs.append(f"Order {oid}: BACKORDER ACCEPTED")


# -----------------------------
# Process One
# -----------------------------
@app.route("/process")
def process():
    consume_one()
    return redirect(url_for("home"))


# -----------------------------
# Auto Process (Thread Pool)
# -----------------------------
@app.route("/auto")
def auto():
    workers = ThreadPoolExecutor(max_workers=3)

    tasks = min(3, len(buffer))

    for _ in range(tasks):
        workers.submit(consume_one)

    workers.shutdown(wait=True)

    logs.append("Thread Pool completed batch processing")

    return redirect(url_for("home"))


# -----------------------------
# CAP Modes
# -----------------------------
@app.route("/consistency")
def consistency():
    global mode
    mode = "CONSISTENCY"
    logs.append("Mode switched to CONSISTENCY")
    return redirect(url_for("home"))


@app.route("/availability")
def availability():
    global mode
    mode = "AVAILABILITY"
    logs.append("Mode switched to AVAILABILITY")
    return redirect(url_for("home"))


# -----------------------------
# Reset
# -----------------------------
@app.route("/reset")
def reset():
    global stock, logs, mode, order_id, buffer
    global empty, full

    stock = 3
    logs = []
    mode = "CONSISTENCY"
    order_id = 101
    buffer = []

    empty = threading.Semaphore(BUFFER_SIZE)
    full = threading.Semaphore(0)

    logs.append("System Reset Complete")

    return redirect(url_for("home"))


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
