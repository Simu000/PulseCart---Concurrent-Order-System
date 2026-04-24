# PulseCart – Concurrent Order Processing System

PulseCart is a Flask-based web application that simulates an e-commerce order processing system. It demonstrates key concepts of concurrency, synchronization, and system performance using the Producer–Consumer model, semaphores, mutex locks, and thread pools. The project bridges theoretical knowledge with practical implementation in a real-world inspired system.

---

## 🚀 Features

- Producer–Consumer model with bounded buffer  
- Thread-safe operations using mutex and semaphores  
- Concurrent order processing using thread pools  
- Async producer simulation using asyncio  
- CAP theorem simulation (Consistency vs Availability)  
- Automated performance and stress testing  
- Docker containerization  
- Cloud deployment (Render)  

---

## 🧠 Concepts Demonstrated

- Concurrency vs Parallelism  
- Thread synchronization and race condition handling  
- Amdahl’s Law (limits of speedup)  
- CAP Theorem trade-offs  
- System bottlenecks and scalability limits  

---

## 🏗️ System Architecture

User (Browser)  
↓  
Flask Web App (Routes)  
↓  
Async Producer (Order Generation)  
↓  
Bounded Buffer (Queue controlled using semaphores)  
↓  
Consumers (Thread Pool Workers)  
↓  
Stock Update (Protected using mutex lock)  

---

## ⚙️ Technologies Used

| Technology | Purpose |
|----------|--------|
| Python | Backend logic |
| Flask | Web framework |
| HTML | UI structure |
| CSS | UI styling |
| threading | Synchronization (mutex, semaphores) |
| concurrent.futures | Thread pool execution |
| asyncio | Async producer simulation |
| requests | Performance testing |
| statistics | Performance analysis |
| Docker | Containerization |
| Render | Cloud deployment |
| Linux (Ubuntu) | Development environment |

---

## 🛠️ Setup Instructions

### Install Dependencies
```bash
pip install flask requests psutil
