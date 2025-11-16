from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts: Mapped[list["Post"]] = db.relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = db.relationship(back_populates="user")
    likes: Mapped[list["Like"]] = db.relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(240))
    caption: Mapped[str] = mapped_column(String(240))
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user: Mapped["User"] = db.relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = db.relationship(back_populates="post")
    likes: Mapped[list["Like"]] = db.relationship(back_populates="post")

    def serialize(self):
        return { 
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption
        } 

class Comment(db.Model): 
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user: Mapped["User"] = db.relationship(back_populates="comments")
    post: Mapped["Post"] = db.relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id, 
            "text": self.text
        }

class Like(db.Model): 
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user: Mapped["User"] = db.relationship(back_populates="likes")
    post: Mapped["Post"] = db.relationship(back_populates="likes")
    

    def serialize(self):
        return {
            "id": self.id
        }
