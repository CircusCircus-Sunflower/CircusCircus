from flask import Flask
# from forum.routes import rt

from forum.auth import auth #NEW LINE imports auth blueprint
from forum.post_routes import post_rt #NEW LINE imports post blueprint
from forum.comments import comments_bp
from flask import Blueprint
from forum.reactions import reactions_bp
from forum.models import embed_media

# Removed comments_bp = Blueprint("comments", __name__) from init for better connection

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    @app.template_filter('embed_media')
    def embed_media_filter(content):
        return embed_media(content)

    # I think more blueprints might be used to break routes up into things like
    # post_routes
    # subforum_routes
    # etc
    # app.register_blueprint(rt)
    app.register_blueprint(auth) #NEW LINE registers auth blueprint
    app.register_blueprint(post_rt) #NEW LINE registers post blueprint
    app.register_blueprint(comments_bp) #NEW LINE registered app blueprint for comments
    app.register_blueprint(reactions_bp) #NEW LINE registered reactions blueprint
    # Set globals
    from forum.models import db
    db.init_app(app)

    with app.app_context():
        # Add some routes
        db.create_all()
        return app


