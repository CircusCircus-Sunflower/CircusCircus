from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from forum.models import User, Post, Comment, Subforum, valid_content, valid_title, db, generateLinkPath, error
from forum.user import username_taken, email_taken, valid_username

##
# This file needs to be broken up into several, to make the project easier to work on.
##

rt = Blueprint('routes', __name__, template_folder='templates')

@rt.route('/action_login', methods=['POST'])
def action_login():
	username = request.form['username']
	password = request.form['password']
	user = User.query.filter(User.username == username).first()
	if user and user.check_password(password):
		login_user(user)
	else:
		errors = []
		errors.append("Username or password is incorrect!")
		return render_template("login.html", errors=errors)
	return redirect("/")


@login_required
@rt.route('/action_logout')
def action_logout():
	#todo
	logout_user()
	return redirect("/")

@rt.route('/action_createaccount', methods=['POST'])
def action_createaccount():
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	errors = []
	retry = False
	if username_taken(username):
		errors.append("Username is already taken!")
		retry=True
	if email_taken(email):
		errors.append("An account already exists with this email!")
		retry = True
	if not valid_username(username):
		errors.append("Username is not valid!")
		retry = True
	# if not valid_password(password):
	# 	errors.append("Password is not valid!")
	# 	retry = True
	if retry:
		return render_template("login.html", errors=errors)
	user = User(email, username, password)
	if user.username == "admin":
		user.admin = True
	db.session.add(user)
	db.session.commit()
	login_user(user)
	return redirect("/")



@rt.route('/loginform')
def loginform():
	return render_template("login.html")


@login_required

@login_required
@rt.route('/action_comment', methods=['POST', 'GET'])
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



