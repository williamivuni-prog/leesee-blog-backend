# Leesee Blog Backend

This is the backend part of my Leesee technical test. I made it with Flask and SQLAlchemy, and it works as a small REST API for the blog frontend.

## Public Repository

- GitHub: `https://github.com/williamivuni-prog/leesee-blog-backend`

## What I Built

- API routes for listing, reading, creating, updating, and deleting posts
- A SQLAlchemy `Post` model
- SQLite for local development
- Support for `DATABASE_URL` if a PostgreSQL database is added later
- CORS setup so the deployed frontend can call the API
- Seed data so the demo has posts right away
- Unit tests with pytest

## How To Run It Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
flask --app run run --debug
```

The API runs at `http://localhost:5000`.

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

## Heroku Option

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

## Links

- Backend: `https://backend-eight-green-11.vercel.app`
- Health check: `https://backend-eight-green-11.vercel.app/api/health`
- Posts API: `https://backend-eight-green-11.vercel.app/api/posts`

## Vercel Deployment

I deployed this backend on Vercel as a Python Function. The repo includes `api/index.py` and `vercel.json` for that.

```bash
vercel deploy --prod
```

For a real production app, I would add a PostgreSQL `DATABASE_URL`. For this test/demo, the deployed version uses SQLite in `/tmp`, which is enough to show the app working but is not meant for permanent data.
