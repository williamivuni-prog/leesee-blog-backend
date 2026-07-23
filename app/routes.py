import re

from flask import Blueprint, request

from .models import Post, db

api = Blueprint("api", __name__)


def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "post"


def validation_error(message):
    return {"error": message}, 400


@api.get("/health")
def health():
    return {"status": "ok"}


@api.get("/posts")
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return {"posts": [post.to_dict() for post in posts], "count": len(posts)}


@api.get("/posts/<slug>")
def get_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return post.to_dict()


@api.post("/posts")
def create_post():
    payload = request.get_json(silent=True) or {}
    required = ["title", "excerpt", "content", "author"]
    missing = [field for field in required if not str(payload.get(field, "")).strip()]
    if missing:
        return validation_error(f"Missing required field(s): {', '.join(missing)}")

    base_slug = slugify(payload["title"])
    slug = base_slug
    suffix = 2
    while Post.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{suffix}"
        suffix += 1

    post = Post(
        title=payload["title"].strip(),
        slug=slug,
        excerpt=payload["excerpt"].strip(),
        content=payload["content"].strip(),
        author=payload["author"].strip(),
    )
    db.session.add(post)
    db.session.commit()
    return post.to_dict(), 201


@api.put("/posts/<slug>")
def update_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    payload = request.get_json(silent=True) or {}

    for field in ["title", "excerpt", "content", "author"]:
        if field in payload:
            value = str(payload[field]).strip()
            if not value:
                return validation_error(f"{field} cannot be empty")
            setattr(post, field, value)

    db.session.commit()
    return post.to_dict()


@api.delete("/posts/<slug>")
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return "", 204
