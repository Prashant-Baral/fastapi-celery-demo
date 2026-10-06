# Async Website Report Generator

A practice mini-project that generates website analysis reports asynchronously. It demonstrates how to integrate FastAPI with Celery and Redis to handle long-running background tasks.

## Features

- **Asynchronous Task Processing:** Uses Celery to perform website scraping without blocking the main API thread.
- **REST API:** Provides FastAPI endpoints to submit a website URL and poll for the report status.
- **Website Metrics:** Uses `httpx` and `BeautifulSoup4` to extract the page title, response time, status code, and the count of links and images on the page.

## Technologies Used

- **FastAPI**: For the web framework and API endpoints.
- **Celery**: For background task queuing and execution.
- **Redis**: As the message broker and backend for Celery.
- **httpx**: For making asynchronous HTTP requests.
- **BeautifulSoup4**: For parsing HTML content.

## Prerequisites

- Python 3.x
- [Redis](https://redis.io/) running locally on default port `6379`.

## Installation

1. Clone or download the repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

You need to run three separate components for the application to work fully:

1. **Start the Redis Server:**
   Ensure your Redis server is running on `localhost:6379`.
   ```bash
   redis-server
   ```

2. **Start the Celery Worker:**
   In a new terminal (with the virtual environment activated), start the Celery worker:
   ```bash
   celery -A celery_app worker --loglevel=info
   ```

3. **Start the FastAPI Application:**
   In another terminal (with the virtual environment activated), start the Uvicorn server:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### 1. Submit a Website for Reporting
- **Endpoint:** `POST /reports?url={url}`
- **Example:**
  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8000/reports?url=https://example.com' \
    -H 'accept: application/json'
  ```
- **Response:**
  ```json
  {
    "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "Pending"
  }
  ```

### 2. Get Report Status and Result
- **Endpoint:** `GET /reports/{job_id}`
- **Example:**
  ```bash
  curl -X 'GET' \
    'http://127.0.0.1:8000/reports/a1b2c3d4-e5f6-7890-abcd-ef1234567890' \
    -H 'accept: application/json'
  ```
- **Response (when completed):**
  ```json
  {
    "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "SUCCESS",
    "result": {
      "url": "https://example.com",
      "status_code": 200,
      "response_time_ms": 150,
      "title": "Example Domain",
      "links": 1,
      "images": 0
    }
  }
  ```

## Disclaimer
This is a small mini-project created for practice and demonstration purposes.
