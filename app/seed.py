from . import create_app
from .models import Post, db
from .sample_data import SAMPLE_POSTS


def seed_database():
    app = create_app()
    with app.app_context():
        for item in SAMPLE_POSTS:
            if not Post.query.filter_by(slug=item["slug"]).first():
                db.session.add(Post(**item))
        db.session.commit()


if __name__ == "__main__":
    seed_database()
    print("Seeded blog posts.")
