# PulseCart – Concurrent Order Processing System

PulseCart is a Flask-based web application that simulates an e-commerce order processing system. It demonstrates key concepts of concurrency, synchronization, and system performance using the Producer–Consumer model, semaphores, mutex locks, and thread pools.

---

## Features

- Producer–Consumer model with bounded buffer
- Thread-safe operations using mutex and semaphores
- Concurrent order processing using thread pools
- Async producer simulation using `asyncio`
- CAP theorem simulation (Consistency vs Availability)
- Performance and stress testing
- Docker containerization
- Cloud deployment (Render)

---

## Concepts Demonstrated

- Concurrency vs Parallelism
- Thread synchronization
- Amdahl’s Law (performance limits)
- CAP Theorem trade-offs
- System bottlenecks and scalability limits

---

## System Architecture
User (Browser)
↓
Flask Web App (Routes)
↓
Producer (Async Orders)
↓
Bounded Buffer (Queue)
↓
Consumers (Thread Pool)
↓
Stock Update (Mutex Protected)


---

## ⚙️ Technologies Used

- Python (Backend logic)
- Flask (Web framework)
- HTML & CSS (Frontend UI)
- threading (Synchronization)
- concurrent.futures (Thread pool)
- asyncio (Async simulation)
- requests (Performance testing)
- Docker (Containerization)
- Render (Cloud deployment)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/pulsecart-concurrent-order-system.git
cd pulsecart-concurrent-order-system
2. Install Dependencies
pip install flask requests psutil
3. Run the Application
python app.py

Open in browser:

http://localhost:5000
