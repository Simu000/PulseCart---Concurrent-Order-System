import queue
import threading
import time

order_queue = queue.Queue()

inventory = {
    "Shoes": 3
}

lock = threading.Lock()

orders = [
    (101, "Shoes"),
    (102, "Shoes"),
    (103, "Shoes"),
    (104, "Shoes"),
    (105, "Shoes")
]

def producer():
    for order in orders:
        print(f"New Order Received: {order}")
        order_queue.put(order)
        time.sleep(0.5)

def consumer():
    while True:
        if not order_queue.empty():
            order = order_queue.get()
            process_order(order)
            order_queue.task_done()
        else:
            break

def process_order(order):
    user_id, item = order

    with lock:
        if inventory[item] > 0:
            inventory[item] -= 1
            print(f"Order {user_id}: SUCCESS")
        else:
            print(f"Order {user_id}: FAILED - Out of Stock")

producer_thread = threading.Thread(target=producer)
consumer1 = threading.Thread(target=consumer)
consumer2 = threading.Thread(target=consumer)

producer_thread.start()
producer_thread.join()

consumer1.start()
consumer2.start()

consumer1.join()
consumer2.join()

print("Final Stock:", inventory["Shoes"])
