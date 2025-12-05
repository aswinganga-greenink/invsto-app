# Invsto Trading API

A high-performance FastAPI application for stock market data management and algorithmic trading strategy backtesting. This project was built as part of the Invsto internship assignment.

## Features

* **FastAPI Backend:** Asynchronous API endpoints for high concurrency.
* **PostgreSQL Database:** Robust data persistence using Prisma ORM.
* **Algorithmic Trading:** Implements a Moving Average Crossover strategy (Golden Cross / Death Cross) using Pandas.
* **Dockerized:** Fully containerized setup with Docker Compose for easy deployment.
* **Unit Testing:** Comprehensive test suite achieving **83% code coverage**.
* **Type Safety:** Strict data validation using Pydantic models (Decimal precision for financial data).

## 🛠️ Tech Stack

* **Language:** Python 3.10
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** Prisma Client Python
* **Data Processing:** Pandas, NumPy
* **Testing:** Unittest, Coverage
* **Deployment:** Docker

---

## Quick Start (Docker)

Make sure that you have a postgres db running and you provided the DATABASE_URL = 'your/postgres:url' in the .env file

### 1. Start the Application
```bash
#clone the repo to your local env
docker build -t invsto-app

### 2. Seed the data
```bash
# make sure to have a data.csv file in the root folder
docker exec -it <container_id> python seed.py

### 3. Api docs
Once the app is running you can access the api docs from
http://localhost:8000/docs

### 4.Running tests
```bash
docker exec -it <container_id> bash
coverage run -m unittest discover -s tests -p "test_*.py" && coverage report -m