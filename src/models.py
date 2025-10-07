from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts: Mapped[list["Post"]] = db.relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = db.relationship("Comment", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(
        String(50), nullable=False)  # e.g., 'image', 'video'
    post_id: Mapped[int] = mapped_column(
        db.ForeignKey('post.id'), nullable=False)
    post: Mapped["Post"] = db.relationship("Post", back_populates="media", uselist=False)
    created_at: Mapped[str] = mapped_column(
        db.DateTime, default=db.func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type,
            "post_id": self.post_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    user: Mapped["User"] = db.relationship("User", back_populates="posts")
    media: Mapped[list["Media"]] = db.relationship("Media", back_populates="post")
    comments: Mapped[list["Comment"]] = db.relationship("Comment", back_populates="post")
    created_at: Mapped[str] = mapped_column(
        db.DateTime, default=db.func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def serialize(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(
        db.ForeignKey('post.id'), nullable=False)
    user: Mapped["User"] = db.relationship("User", back_populates="comments")
    post: Mapped["Post"] = db.relationship("Post", back_populates="comments")
    created_at: Mapped[str] = mapped_column(
        db.DateTime, default=db.func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    user_to: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    created_at: Mapped[str] = mapped_column(
        db.DateTime, default=db.func.current_timestamp())

    def serialize(self):
        return {
            "id": self.id,
            "user_from": self.user_from,
            "user_to": self.user_to,
            "created_at": self.created_at,
        }


class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(
        db.ForeignKey('post.id'), nullable=False)
    created_at: Mapped[str] = mapped_column(
        db.DateTime, default=db.func.current_timestamp())

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at,
        }


class SavedPost(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(
        db.ForeignKey('post.id'), nullable=False)
    created_at: Mapped[str] = mapped_column(
        db.DateTime, default=db.func.current_timestamp())

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at,
        }
