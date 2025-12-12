from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from forum.models import User, Post, Comment, Subforum, valid_content, valid_title, db, generateLinkPath, error




comments_bp = Blueprint("comments", __name__)


@login_required
@comments_bp.route('/action_comment', methods=['POST', 'GET'])
def comment():
	post_id = int(request.args.get("post"))
	post = Post.query.filter(Post.id == post_id).first()
	if not post:
		return error("That post does not exist!")
	content = request.form['content']
	postdate = datetime.datetime.now()
	comment = Comment(content, postdate)
	current_user.comments.append(comment)
	post.comments.append(comment)
	db.session.commit()
	return redirect("/viewpost?post=" + str(post_id))

@comments_bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
	comment = Comment.query.get(comment_id)
	if not comment:
		return error("Comment not found!")
	if comment.user_id != current_user.id:
		return error("You can only delete your own comments!")
	
	post_id = comment.post_id
	db.session.delete(comment)
	db.session.commit()
	return redirect("/viewpost?post=" + str(post_id))

# Top two code blocks "def comment" & "def delete" have been added, ran and tested.

# Moved to a new Port to solve running issues "Port 5002"