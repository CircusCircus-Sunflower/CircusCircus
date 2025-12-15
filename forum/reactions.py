from flask import Blueprint, redirect, jsonify
from flask_login import current_user
from flask_login.utils import login_required
from forum.models import Reaction, Post, db, error

reactions_bp = Blueprint("reactions", __name__)

@reactions_bp.route("/react/<int:post_id>/<reaction_type>", methods=["POST"])
@login_required
def react(post_id, reaction_type):
    # 1) validate reaction_type
    if reaction_type not in ["like", "dislike", "heart"]:
        return error("Invalid reaction_type!")
    # 2) validate post exists
    post = Post.query.get(post_id)
    if not post:
        return error("Post not found!")
    # 3) find existing reaction by this user for the post
    existing = Reaction.query.filter_by(
        user_id = current_user.id,
        post_id = post_id
    ).first()
    # 4) same reaction=remove, different reaction=update, toggle/switch
    if existing:
        if existing.reaction_type == reaction_type:
            db.session.delete(existing) #toggle off
        else:
            existing.reaction_type = reaction_type #switch
    else:
        reaction = Reaction(
            user_id = current_user.id,
            post_id = post_id,
            reaction_type = reaction_type
        )
        db.session.add(reaction)
    # 5) persist
    db.session.commit()
    # 6) return user to the post page
    return redirect("/viewpost?post=" + str(post_id))

@reactions_bp.route("/reactions/<int:post_id>", methods=["GET"])
def get_reactions(post_id):
    likes = Reaction.query.filter_by(post_id=post_id, reaction_type="like").count()
    dislikes = Reaction.query.filter_by(post_id=post_id, reaction_type="dislike").count()
    hearts = Reaction.query.filter_by(post_id=post_id, reaction_type="heart").count()

    return jsonify({
        "likes": likes,
        "dislikes": dislikes,
        "hearts": hearts
    })