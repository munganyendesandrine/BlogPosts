from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    def __repr__(self):
        return f'User {self.username}'    

class BlogPost(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    blog = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer,db.ForeignKey('comments.id'))

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def fetch_blogs():
        blogs= BlogPost.query.all()
        return blogs 
        
    def __repr__(self):
        return f'BlogPost {self.name}'           


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))

    # @classmethod
    # def get_comments(cls,id):
    #   comments=Comment.query.filter_by(blog_id=id).all()
    #   return comments

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def fetch_comment():
        comment= Comment.query.all()
        return comment   
        
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()
   

    def __repr__(self):
        return f'Comment {self.name}' 


