import os

from flask import Flask
from flask_cors import CORS

from .models import db
from .routes import api
from .sample_data import SAMPLE_POSTS


def create_app(test_config=None):
    app = Flask(__name__)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        database_url = "sqlite:////tmp/blog.db" if os.getenv("VERCEL") else "sqlite:///blog.db"
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "*")}})
    app.register_blueprint(api, url_prefix="/api")

    @app.get("/")
    def index():
        return {
            "name": "Leesee Blog API",
            "status": "ok",
            "docs": "/api/posts",
        }

    with app.app_context():
        db.create_all()
        should_seed = os.getenv("AUTO_SEED", "1" if os.getenv("VERCEL") else "0") == "1"
        if should_seed:
            from .models import Post

            for item in SAMPLE_POSTS:
                if not Post.query.filter_by(slug=item["slug"]).first():
                    db.session.add(Post(**item))
            db.session.commit()

    return app
