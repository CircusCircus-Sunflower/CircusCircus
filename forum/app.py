
from flask import render_template
from flask_login import LoginManager
from forum.models import Subforum, db, User

from . import create_app
app = create_app()

app.config['SITE_NAME'] = 'Mumble'
app.config['SITE_DESCRIPTION'] = 'A Pop Culture & Technology Forum'
app.config['FLASK_DEBUG'] = 1

def init_site():
	print("creating initial subforums")
	admin = add_subforum("The Mumble Room", "Where announcements, updates, and general discussion live")
	add_subforum("The Drop", "Official updates, releases, and community notices",admin)
	add_subforum("Tech Support & Bugs", "Report issues, glitches, and technical problems", admin)
	add_subforum("Open Mic", "Talk about anything pop culture, tech, or trending")
	add_subforum("Off the Record", "Everything that doesn't fit anywhere else")

def add_subforum(title, description, parent=None):
	sub = Subforum(title, description)
	if parent:
		for subforum in parent.subforums:
			if subforum.title == title:
				return
		parent.subforums.append(sub)
	else:
		subforums = Subforum.query.filter(Subforum.parent_id == None).all()
		for subforum in subforums:
			if subforum.title == title:
				return
		db.session.add(sub)
	print("adding " + title)
	db.session.commit()
	return sub

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)

with app.app_context():
	db.create_all() # TODO this may be redundant
	if not Subforum.query.all():
		init_site()

@app.route('/')
def index():
	subforums = Subforum.query.filter(Subforum.parent_id == None).order_by(Subforum.id)
	return render_template("subforums.html", subforums=subforums)




