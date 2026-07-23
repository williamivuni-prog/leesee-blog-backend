# Leesee Blog Backend

Flask + SQLAlchemy REST API for a simple blog technical test.

## Features

- REST endpoints for listing, reading, creating, updating, and deleting posts
- SQLite for local development
- `DATABASE_URL` support for PostgreSQL-compatible cloud databases
- CORS configuration for the deployed frontend
- Pytest unit tests
- Heroku-ready `Procfile`

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
flask --app run run --debug
```

The API will run at `http://localhost:5000`.

## API Routes

- `GET /api/health`
- `GET /api/posts`
- `GET /api/posts/<slug>`
- `POST /api/posts`
- `PUT /api/posts/<slug>`
- `DELETE /api/posts/<slug>`

## Tests

```bash
pytest
```

## Deploy To Heroku

```bash
heroku create leesee-blog-api
heroku addons:create heroku-postgresql:essential-0
heroku config:set CORS_ORIGINS=https://your-vercel-app.vercel.app
git push heroku main
```

After deployment, seed sample data if desired:

```bash
heroku run python -m app.seed
```

## Deployment URL

Replace this after deployment:

- Backend: `https://your-backend-app.herokuapp.com`

## Deploy To Vercel

This repository also includes `api/index.py` and `vercel.json`, so it can run as a Vercel Python Function:

```bash
vercel deploy --prod
```

For a production database, add a PostgreSQL `DATABASE_URL`. Without one, the Vercel deployment uses SQLite in `/tmp`, which is enough for a live demo but not durable storage.
