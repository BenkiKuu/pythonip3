from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(250), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    postcomments = db.relationship('CommentsPost', backref='author', lazy=True)
    pickup = db.relationship('Pickup', backref='author', lazy=True)
    pickupcomments = db.relationship('CommentsPickup', backref='author', lazy=True)
    product = db.relationship('Product', backref='author', lazy=True)
    productcomments = db.relationship('CommentsProduct', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    content= db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('CommentsPost', backref='title', lazy='dynamic')


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class CommentsPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"CommentsPost('{self.comment}', '{self.date_posted}')"

class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    content= db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('CommentsPickup', backref='title', lazy='dynamic')
    def __repr__(self):
        return f"PickUp('{self.title}', '{self.date_posted}')"

class CommentsPickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    pickup_id = db.Column(db.Integer, db.ForeignKey("pickup.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"CommentsPickup('{self.comment}', '{self.date_posted}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    content= db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('CommentsProduct', backref='title', lazy='dynamic')

    def __repr__(self):
        return f"Product('{self.title}', '{self.date_posted}')"

class CommentsProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"CommentsProduct('{self.comment}', '{self.date_posted}')"
