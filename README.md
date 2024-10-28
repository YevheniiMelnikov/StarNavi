## Description

StarNavi test task made with Django

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YevheniiMelnikov/StarNavi
```

### 2. Create .env file with following variables:

```bash
DB_NAME  
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
DEBUG_STATUS
SECRET_KEY
OPENAI_API_KEY
EMAIL_HOST_USER
DEFAULT_FROM_EMAIL
EMAIL_HOST_PASSWORD
CELERY_BROKER_URL
REDIS_HOST
REDIS_PORT
```

### 3. Running the project

```bash
docker-compose up --build
```

### 4. Usage
Go to http://localhost:8000/swagger/ to see API docs