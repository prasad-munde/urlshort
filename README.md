# URL Shortener

A URL shortening backend built with FastAPI, PostgreSQL, and Redis. Supports unique short-code generation, optional expiration, Redis caching, and rate limiting.

## Features

- URL shortening with Pydantic validation
- Unique short-code generation
- PostgreSQL persistence
- Optional URL expiration
- Redis caching (cache-aside pattern)
- Redis-based rate limiting (fixed window)
- Structured logging
- Environment-based configuration
- Auto-generated Swagger/ReDoc docs

## Tech Stack

| Technology | Purpose |
|---|---|
| Python / FastAPI | REST API |
| PostgreSQL | Persistent storage |
| SQLAlchemy | ORM |
| Redis | Caching & rate limiting |
| Pydantic | Request/response validation |
| Docker / Docker Compose | Containerization |

## Architecture

```
Client → FastAPI Backend → Redis (cache + rate limit)
                          → PostgreSQL (URLs + metadata)
```

## API

### `POST /shorten`
Creates a shortened URL.

**Request**
```json
{ "mainurl": "https://www.example.com/very/long/url" }
```

**Response**
```json
{
  "original_url": "https://www.example.com/very/long/url",
  "short_code": "aX72kP",
  "expires_at": null,
  "created_at": "2026-08-23T22:30:00"
}
```

### `GET /{short_code}`
Redirects to the original URL. Checks Redis first (cache-aside); on a miss, falls back to PostgreSQL and repopulates the cache.

```
Redis HIT  → redirect
Redis MISS → PostgreSQL → store in Redis → redirect
```

### Rate Limiting
100 requests / 60-second window per client, enforced with Redis `INCR` for atomic counting.

### Error Responses

| Status | Case | Body |
|---|---|---|
| 404 | URL not found | `{"detail": "URL not found"}` |
| 410 | URL expired | `{"detail": "Url has Expired"}` |
| 429 | Rate limit exceeded | `{"detail": "Too many requests"}` |

## Project Structure

```
urlshortner/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   ├── redis.py
│   ├── rate_limiter.py
│   ├── logging_config.py
│   └── utils.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## Running the Project

**Prerequisites:** Python 3.12+, Docker, Docker Compose

```bash
git clone YOUR_REPOSITORY_URL
cd urlshortner
docker compose up --build
```

API available at `http://localhost:8000`. Interactive docs at `/docs` (Swagger) or `/redoc`.

**Local development** (without Docker):
```bash
uvicorn app.main:app --reload
```

### Environment Variables

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=url_shortener
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/url_shortener
REDIS_HOST=redis
REDIS_PORT=6379
```

## Future Improvements

- JWT authentication and user-owned URLs
- Click analytics
- Background jobs with Celery
- Nginx reverse proxy
- CI/CD and monitoring
- Alembic migrations

## License

Built for learning and portfolio purposes.