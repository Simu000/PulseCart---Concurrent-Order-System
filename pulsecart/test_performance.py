import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:5000"

WORKLOADS = [5000]
RUNS = 3

PRODUCTS = ["laptop", "mouse", "keyboard", "monitor", "headphones"]


# -----------------------------
# Reset system
# -----------------------------
def reset_system():
    try:
        requests.get(f"{BASE_URL}/reset")
    except:
        print("Reset failed")


# -----------------------------
# Add order
# -----------------------------
def add_order(product):
    try:
        requests.post(f"{BASE_URL}/add", json={"product": product, "quantity": 1})
        return True
    except:
        return False


# -----------------------------
# Process repeatedly until done
# -----------------------------
def process_until_empty():
    for _ in range(50):  # max cycles (safety limit)
        try:
            requests.get(f"{BASE_URL}/auto")
        except:
            pass

        time.sleep(0.2)

        # check queue
        try:
            res = requests.get(BASE_URL)
            if "<h2>0</h2>" in res.text:
                return True
        except:
            pass

    return False


# -----------------------------
# Run single workload
# -----------------------------
def run_test(order_count):
    reset_system()
    time.sleep(0.5)

    start = time.time()

    def task(i):
        product = PRODUCTS[i % len(PRODUCTS)]
        return add_order(product)

    # Add orders concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(task, range(order_count)))

    success = results.count(True)
    fail = results.count(False)

    # Process automatically until done
    done = process_until_empty()

    if done:
        end = time.time()
        return end - start, success, fail
    else:
        return None, success, fail


# -----------------------------
# Main test runner
# -----------------------------
def main():
    print("PulseCart Performance Test\n")

    all_results = []

    for workload in WORKLOADS:
        print(f"\nTesting {workload} orders")

        times = []

        for i in range(RUNS):
            print(f"Run {i+1}...", end=" ")

            elapsed, success, fail = run_test(workload)

            if elapsed:
                print(f"{elapsed:.2f}s (success={success}, fail={fail})")
                times.append(elapsed)
            else:
                print("Timeout")

            time.sleep(1)

        if times:
            avg = statistics.mean(times)
            all_results.append((workload, times, avg))

    # -----------------------------
    # Results summary
    # -----------------------------
    print("\n--- RESULTS ---")

    baseline = all_results[0][2]

    for workload, times, avg in all_results:
        speedup = baseline / avg if avg > 0 else 0

        print(f"\nWorkload: {workload}")
        print(f"Times: {times}")
        print(f"Average: {avg:.2f}s")
        print(f"Speedup: {speedup:.2f}x")


if __name__ == "__main__":
    main()
