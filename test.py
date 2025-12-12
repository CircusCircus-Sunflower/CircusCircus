"""
CircusCircus Test Suite
Run with: pytest test.py -v
"""

import pytest
import datetime
from forum import create_app
from forum.models import db, User, Post, Comment, Reaction, Subforum, valid_title, valid_content


# ============== FIXTURES ==============

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for tests
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User("test@example.com", "testuser", "password123")
        db.session.add(user)
        db.session.commit()
        return user.id  # Return ID since object won't persist outside context


@pytest.fixture
def sample_subforum(app):
    """Create a sample subforum for testing."""
    with app.app_context():
        subforum = Subforum("Test Forum", "A test subforum")
        db.session.add(subforum)
        db.session.commit()
        return subforum.id


@pytest.fixture
def sample_post(app, sample_user, sample_subforum):
    """Create a sample post for testing."""
    with app.app_context():
        user = User.query.get(sample_user)
        subforum = Subforum.query.get(sample_subforum)
        post = Post("Test Post Title", "This is test content for the post.", datetime.datetime.now())
        post.user_id = user.id
        post.subforum_id = subforum.id
        db.session.add(post)
        db.session.commit()
        return post.id


# ============== MODEL TESTS ==============

class TestUserModel:
    """Tests for User model."""

    def test_create_user(self, app):
        """Test creating a new user."""
        with app.app_context():
            user = User("john@example.com", "johndoe", "securepass")
            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.username == "johndoe"
            assert user.email == "john@example.com"

    def test_password_hashing(self, app):
        """Test that password is hashed and can be verified."""
        with app.app_context():
            user = User("jane@example.com", "janedoe", "mypassword")
            db.session.add(user)
            db.session.commit()

            # Password should be hashed, not stored as plain text
            assert user.password_hash != "mypassword"
            # check_password should return True for correct password
            assert user.check_password("mypassword") == True
            # check_password should return False for wrong password
            assert user.check_password("wrongpassword") == False

    def test_user_default_not_admin(self, app):
        """Test that new users are not admins by default."""
        with app.app_context():
            user = User("user@example.com", "regularuser", "password")
            db.session.add(user)
            db.session.commit()

            assert user.admin == False


class TestPostModel:
    """Tests for Post model."""

    def test_create_post(self, app, sample_user, sample_subforum):
        """Test creating a new post."""
        with app.app_context():
            post = Post("My First Post", "This is the content of my post.", datetime.datetime.now())
            post.user_id = sample_user
            post.subforum_id = sample_subforum
            db.session.add(post)
            db.session.commit()

            assert post.id is not None
            assert post.title == "My First Post"
            assert post.content == "This is the content of my post."

    def test_post_time_string(self, app, sample_user, sample_subforum):
        """Test that get_time_string returns a string."""
        with app.app_context():
            post = Post("Test Post", "Content here", datetime.datetime.now())
            post.user_id = sample_user
            post.subforum_id = sample_subforum
            db.session.add(post)
            db.session.commit()

            time_string = post.get_time_string()
            assert isinstance(time_string, str)
            assert "ago" in time_string or "moment" in time_string


class TestCommentModel:
    """Tests for Comment model."""

    def test_create_comment(self, app, sample_post, sample_user):
        """Test creating a comment on a post."""
        with app.app_context():
            comment = Comment("This is a test comment!", datetime.datetime.now())
            comment.user_id = sample_user
            comment.post_id = sample_post
            db.session.add(comment)
            db.session.commit()

            assert comment.id is not None
            assert comment.content == "This is a test comment!"

    def test_comment_belongs_to_post(self, app, sample_post, sample_user):
        """Test that comment is linked to post."""
        with app.app_context():
            comment = Comment("Another comment", datetime.datetime.now())
            comment.user_id = sample_user
            comment.post_id = sample_post
            db.session.add(comment)
            db.session.commit()

            post = Post.query.get(sample_post)
            assert len(post.comments) == 1
            assert post.comments[0].content == "Another comment"


class TestReactionModel:
    """Tests for Reaction model."""

    def test_create_reaction(self, app, sample_post, sample_user):
        """Test creating a reaction on a post."""
        with app.app_context():
            reaction = Reaction(sample_user, sample_post, "like")
            db.session.add(reaction)
            db.session.commit()

            assert reaction.id is not None
            assert reaction.reaction_type == "like"
            assert reaction.user_id == sample_user
            assert reaction.post_id == sample_post

    def test_reaction_types(self, app, sample_post, sample_user):
        """Test different reaction types."""
        with app.app_context():
            # Test like
            reaction1 = Reaction(sample_user, sample_post, "like")
            db.session.add(reaction1)
            db.session.commit()
            assert reaction1.reaction_type == "like"

            # Clean up for next test
            db.session.delete(reaction1)
            db.session.commit()

            # Test dislike
            reaction2 = Reaction(sample_user, sample_post, "dislike")
            db.session.add(reaction2)
            db.session.commit()
            assert reaction2.reaction_type == "dislike"

            # Clean up
            db.session.delete(reaction2)
            db.session.commit()

            # Test heart
            reaction3 = Reaction(sample_user, sample_post, "heart")
            db.session.add(reaction3)
            db.session.commit()
            assert reaction3.reaction_type == "heart"

    def test_reaction_unique_constraint(self, app, sample_post, sample_user):
        """Test that user can only have one reaction per post."""
        with app.app_context():
            reaction1 = Reaction(sample_user, sample_post, "like")
            db.session.add(reaction1)
            db.session.commit()

            # Trying to add another reaction from same user to same post should fail
            reaction2 = Reaction(sample_user, sample_post, "heart")
            db.session.add(reaction2)

            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()

    def test_reaction_belongs_to_post(self, app, sample_post, sample_user):
        """Test that reaction is linked to post."""
        with app.app_context():
            reaction = Reaction(sample_user, sample_post, "like")
            db.session.add(reaction)
            db.session.commit()

            post = Post.query.get(sample_post)
            assert len(post.reactions) == 1
            assert post.reactions[0].reaction_type == "like"


class TestSubforumModel:
    """Tests for Subforum model."""

    def test_create_subforum(self, app):
        """Test creating a subforum."""
        with app.app_context():
            subforum = Subforum("General Discussion", "Talk about anything")
            db.session.add(subforum)
            db.session.commit()

            assert subforum.id is not None
            assert subforum.title == "General Discussion"
            assert subforum.description == "Talk about anything"


# ============== VALIDATION TESTS ==============

class TestValidation:
    """Tests for validation functions."""

    def test_valid_title(self):
        """Test title validation."""
        # Too short
        assert valid_title("Hi") == False
        assert valid_title("Hey") == False

        # Valid
        assert valid_title("Hello World") == True
        assert valid_title("This is a valid title") == True

        # Too long (over 140 chars)
        long_title = "x" * 141
        assert valid_title(long_title) == False

    def test_valid_content(self):
        """Test content validation."""
        # Too short
        assert valid_content("Short") == False
        assert valid_content("Too small") == False

        # Valid
        assert valid_content("This is valid content for a post.") == True

        # Too long (over 5000 chars)
        long_content = "x" * 5001
        assert valid_content(long_content) == False


# ============== ROUTE TESTS ==============

class TestRoutes:
    """Tests for application routes."""

    def test_home_page(self, client):
        """Test that home page loads."""
        response = client.get('/')
        assert response.status_code == 200

    def test_login_page(self, client):
        """Test that login page loads."""
        response = client.get('/loginform')
        assert response.status_code == 200

    def test_subforum_page(self, client, sample_subforum):
        """Test that subforum page loads."""
        response = client.get(f'/subforum?sub={sample_subforum}')
        assert response.status_code == 200

    def test_viewpost_page(self, client, sample_post):
        """Test that view post page loads."""
        response = client.get(f'/viewpost?post={sample_post}')
        assert response.status_code == 200

    def test_invalid_subforum(self, client):
        """Test accessing non-existent subforum."""
        response = client.get('/subforum?sub=99999')
        assert b"does not exist" in response.data

    def test_invalid_post(self, client):
        """Test accessing non-existent post."""
        response = client.get('/viewpost?post=99999')
        assert b"does not exist" in response.data


# ============== RUN TESTS ==============

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
