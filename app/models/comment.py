import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apiflask import Schema
from apiflask.fields import String, Integer, Boolean
from operator import attrgetter
from typing import List

from .base import Base as BaseModel

class CommentInput(Schema):
    author_id = Integer()
    text = String()
    approved = Boolean()


class CommentOutput(CommentInput):
    pass


class Comment(BaseModel):

    json_fields:List[str]  = ['text', 'author.username', 'blog.title']

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    text: Mapped[str] = mapped_column(sa.String(255))
    approved: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    blog_id: Mapped[int] = mapped_column(ForeignKey('blogs.id'))

    blog: Mapped["Blog"] = relationship("Blog", back_populates='comments')
    author:Mapped["User"] = relationship("User", back_populates='comments')

    def __repr__(self):
        return f'''
            {self.text}
            by: {self.author.username}
        '''



    @staticmethod
    def approve_comments(comments):
        for comment in comments:
            comment.approved = True
            comment.save()
