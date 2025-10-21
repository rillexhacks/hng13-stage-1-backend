# String Analyzer Service

A RESTful API service that analyzes strings and stores their computed properties. Built with **Python** and **FastAPI**, and deployed on **Render**.

**Live Application:** [https://hng13-stage-1-backend.onrender.com/](https://hng13-stage-1-backend.onrender.com/)

---

## Table of Contents

- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running Locally](#running-locally)
- [Dependencies](#dependencies)
- [Testing](#testing)
- [Deployment](#deployment)
- [License](#license)

---

## Features

For each analyzed string, the service computes and stores:

- `length`: Number of characters in the string
- `is_palindrome`: Boolean indicating if the string reads the same forwards and backwards (case-insensitive)
- `unique_characters`: Count of distinct characters
- `word_count`: Number of words separated by whitespace
- `sha256_hash`: SHA-256 hash of the string (unique ID)
- `character_frequency_map`: Dictionary mapping each character to its occurrence count

Supports:

- Creating and analyzing strings
- Fetching strings by value
- Filtering strings with query parameters
- Natural language filtering
- Deleting strings

---

## API Endpoints

All endpoints are available at the live URL:  
[https://hng13-stage-1-backend.onrender.com/](https://hng13-stage-1-backend.onrender.com/)

### 1. Create / Analyze String

**POST** `/strings`  
**Full URL:** `https://hng13-stage-1-backend.onrender.com/strings`  

**Request Body:**
```json
{
  "value": "string to analyze"
}
Success Response (201 Created):

json
Copy code
{
  "id": "sha256_hash_value",
  "value": "string to analyze",
  "properties": {
    "length": 17,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "abc123...",
    "character_frequency_map": {
      "s": 2,
      "t": 3
    }
  },
  "created_at": "2025-08-27T10:00:00Z"
}
Errors:

409 Conflict – String already exists

400 Bad Request – Invalid or missing "value"

422 Unprocessable Entity – Invalid data type

2. Get Specific String
GET /strings/{string_value}
Full URL Example: https://hng13-stage-1-backend.onrender.com/strings/racecar

Success Response (200 OK):

json
Copy code
{
  "id": "sha256_hash_value",
  "value": "racecar",
  "properties": { /* same as above */ },
  "created_at": "2025-08-27T10:00:00Z"
}
Errors:

404 Not Found – String not found

3. Get All Strings with Filtering
GET /strings
Full URL Example:
https://hng13-stage-1-backend.onrender.com/strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a

Query Parameters:

is_palindrome: boolean

min_length: integer

max_length: integer

word_count: integer

contains_character: string (single character)

Success Response (200 OK):

json
Copy code
{
  "data": [
    { /* string objects */ }
  ],
  "count": 15,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "max_length": 20,
    "word_count": 2,
    "contains_character": "a"
  }
}
Errors:

400 Bad Request – Invalid query parameters

4. Natural Language Filtering
GET /strings/filter-by-natural-language
Full URL Example:
https://hng13-stage-1-backend.onrender.com/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings

Success Response (200 OK):

json
Copy code
{
  "data": [ /* array of matching strings */ ],
  "count": 3,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
Errors:

400 Bad Request – Unable to parse query

422 Unprocessable Entity – Conflicting filters

5. Delete String
DELETE /strings/{string_value}
Full URL Example: https://hng13-stage-1-backend.onrender.com/strings/racecar

Success Response (204 No Content)

Error:

404 Not Found – String does not exist

Getting Started
Prerequisites
Python 3.10+

pip

Git

Installation
Clone the repo:

bash
Copy code
git clone https://github.com/rillexhacks/hng13-stage-1-backend.git
Create a virtual environment and activate it:

bash
Copy code
python -m venv .env
source .env/bin/activate  # Linux/Mac
.env\Scripts\activate     # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Environment Variables
Create a .env file in the root directory:

dotenv
Copy code
DATABASE_URL=sqlite:///./strings.db
Replace with your database URL if using PostgreSQL, MySQL, etc.

Running Locally
bash
Copy code
uvicorn main:app --reload
API will be available at http://127.0.0.1:8000

Interactive API docs available at:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Dependencies
FastAPI

Uvicorn

Pydantic

python-dotenv

hashlib (built-in)

Install all via:

bash
Copy code
pip install -r requirements.txt
Testing
You can test endpoints using:

Postman

curl

Interactive API docs (/docs or /redoc)

Example:

bash
Copy code
curl -X POST "https://hng13-stage-1-backend.onrender.com/strings" \
-H "Content-Type: application/json" \
-d '{"value":"racecar"}'
Deployment
This project is deployed on Render:

Push your code to GitHub.

Create a new web service on Render.

Connect your GitHub repository.

Set environment variables.

Select Python build environment.

Deploy and access your live API URL.