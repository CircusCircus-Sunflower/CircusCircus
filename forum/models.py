
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
import re

# create db here so it can be imported (with the models) into the App object.
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#OBJECT MODELS
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password_hash = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    admin = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comment", backref="user")
    reactions = db.relationship("Reaction", backref="user")

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    comments = db.relationship("Comment", backref="post")
    reactions = db.relationship("Reaction", backref="post") #Reactions added
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subforum_id = db.Column(db.Integer, db.ForeignKey('subforum.id'))
    postdate = db.Column(db.DateTime)

    #cache stuff
    lastcheck = None
    savedresponce = None
    def __init__(self, title, content, postdate):
        self.title = title
        self.content = content
        self.postdate = postdate
    def get_time_string(self):
        #this only needs to be calculated every so often, not for every request
        #this can be a rudamentary chache
        now = datetime.datetime.now()
        if self.lastcheck is None or (now - self.lastcheck).total_seconds() > 30:
            self.lastcheck = now
        else:
            return self.savedresponce

        diff = now - self.postdate

        seconds = diff.total_seconds()
        print(seconds)
        if seconds / (60 * 60 * 24 * 30) > 1:
            self.savedresponce =  " " + str(int(seconds / (60 * 60 * 24 * 30))) + " months ago"
        elif seconds / (60 * 60 * 24) > 1:
            self.savedresponce =  " " + str(int(seconds / (60*  60 * 24))) + " days ago"
        elif seconds / (60 * 60) > 1:
            self.savedresponce = " " + str(int(seconds / (60 * 60))) + " hours ago"
        elif seconds / (60) > 1:
            self.savedresponce = " " + str(int(seconds / 60)) + " minutes ago"
        else:
            self.savedresponce =  "Just a moment ago!"

        return self.savedresponce

class Subforum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    subforums = db.relationship("Subforum")
    parent_id = db.Column(db.Integer, db.ForeignKey('subforum.id'))
    posts = db.relationship("Post", backref="subforum")
    path = None
    hidden = db.Column(db.Boolean, default=False)
    def __init__(self, title, description):
        self.title = title
        self.description = description

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    postdate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    lastcheck = None
    savedresponce = None
    def __init__(self, content, postdate):
        self.content = content
        self.postdate = postdate
    def get_time_string(self):
        #this only needs to be calculated every so often, not for every request
        #this can be a rudamentary chache
        now = datetime.datetime.now()
        if self.lastcheck is None or (now - self.lastcheck).total_seconds() > 30:
            self.lastcheck = now
        else:
            return self.savedresponce

        diff = now - self.postdate
        seconds = diff.total_seconds()
        if seconds / (60 * 60 * 24 * 30) > 1:
            self.savedresponce =  " " + str(int(seconds / (60 * 60 * 24 * 30))) + " months ago"
        elif seconds / (60 * 60 * 24) > 1:
            self.savedresponce =  " " + str(int(seconds / (60*  60 * 24))) + " days ago"
        elif seconds / (60 * 60) > 1:
            self.savedresponce = " " + str(int(seconds / (60 * 60))) + " hours ago"
        elif seconds / (60) > 1:
            self.savedresponce = " " + str(int(seconds / 60)) + " minutes ago"
        else:
            self.savedresponce =  "Just a moment ago!"
        return self.savedresponce

class Reaction(db.Model):#added class Reaction
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id= db.Column(db.Integer,db.ForeignKey('post.id'), nullable= False)
    reaction_type= db.Column(db.String(20), nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_reaction'),)


    def __init__(self,user_id,post_id,reaction_type):
        self.user_id = user_id
        self.post_id= post_id
        self.reaction_type= reaction_type


def error(errormessage):
	return "<b style=\"color: red;\">" + errormessage + "</b>"

def generateLinkPath(subforumid):
	links = []
	subforum = Subforum.query.filter(Subforum.id == subforumid).first()
	parent = Subforum.query.filter(Subforum.id == subforum.parent_id).first()
	links.append("<a href=\"/subforum?sub=" + str(subforum.id) + "\">" + subforum.title + "</a>")
	while parent is not None:
		links.append("<a href=\"/subforum?sub=" + str(parent.id) + "\">" + parent.title + "</a>")
		parent = Subforum.query.filter(Subforum.id == parent.parent_id).first()
	links.append("<a href=\"/\">Forum Index</a>")
	link = ""
	for l in reversed(links):
		link = link + " / " + l
	return link

#Post checks
def valid_title(title):
	return len(title) > 4 and len(title) < 140
def valid_content(content):
	return len(content) > 10 and len(content) < 5000

#embed media
#https://developers.google.com/youtube/player_parameters
#from apple https://embed.music.apple.com/us/album/ALBUM_NAME/ALBUM_ID?i=SONG_ID

def embed_media(content):
    """Convert YouTube and Apple Music links to embedded players."""
    # YouTube: https://www.youtube.com/watch?v=VIDEO_ID
    youtube_pattern = r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
    content = re.sub(#finds the function and replaces it with <iframe>
        youtube_pattern,
        r'<iframe width="560" height="315" src="https://www.youtube.com/embed/\1" frameborder="0" allowfullscreen></iframe>',
        content
    )
    # YouTube short: https://youtu.be/VIDEO_ID
    youtube_short_pattern = r'https?://youtu\.be/([a-zA-Z0-9_-]+)'
    content = re.sub(
        youtube_short_pattern,
        r'<iframe width="560" height="315" src="https://www.youtube.com/embed/\1" frameborder="0" allowfullscreen></iframe>',
        content
    )
    # Apple Music song: https://music.apple.com/us/album/song-name/ALBUM_ID?i=SONG_ID
    apple_music_pattern = r'https?://music\.apple\.com/(\w+)/album/[^/]+/(\d+)\?i=(\d+)'
    content = re.sub(
        apple_music_pattern,
        r'<iframe allow="autoplay *; encrypted-media *;" frameborder="0" height="150" style="width:100%;max-width:660px;overflow:hidden;background:transparent;" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-storage-access-by-user-activation allow-top-navigation-by-user-activation" src="https://embed.music.apple.com/\1/album/\2?i=\3"></iframe>',
        content
    )
    # Apple Music album: https://music.apple.com/us/album/album-name/ALBUM_ID
    apple_album_pattern = r'https?://music\.apple\.com/(\w+)/album/[^/]+/(\d+)(?!\?)'
    content = re.sub(
        apple_album_pattern,
        r'<iframe allow="autoplay *; encrypted-media *;" frameborder="0" height="450" style="width:100%;max-width:660px;overflow:hidden;background:transparent;" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-storage-access-by-user-activation allow-top-navigation-by-user-activation" src="https://embed.music.apple.com/\1/album/\2"></iframe>',
        content
    )
    return content