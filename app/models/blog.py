from datetime import datetime
from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apiflask import Schema
from apiflask.fields import String, Integer, DateTime, Enum as EnumField

from .base import Base as BaseModel
#from models.joins import tag_blogs
from .shared import Status


class BlogInput(Schema):
    title = String()
    status = EnumField(Status)
    author_id = Integer()
    content = String()
    slug = String()


class BlogOutput(Schema):
    title = String()
    status = EnumField(Status)
    author_id = Integer()
    content = String()
    slug = String()
    published_date = DateTime()


class Blog(BaseModel):

    json_fields = [
        'title',
        'slug',
        'author.username',
        'published_date',
    ]

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(255))
    status: Mapped[Status] = mapped_column(
            sa.Enum(Status), 
            default="draft"
    )
    author_id = mapped_column(sa.ForeignKey('users.id', name='blog_usersid_fk'))
    author: Mapped["User"] = relationship(
                'User', 
                back_populates='blogs'
            )
        
    content: Mapped[str] = mapped_column(sa.Text)   
    slug: Mapped[str] = mapped_column(sa.String(255))
    published_date: Mapped[datetime] = mapped_column(sa.DateTime)
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates='blog')  
    pages: Mapped[List['Page']] = relationship('Page', back_populates='blog')

#    tags: Mapped[List["Tag"]] = relationship(secondary=tag_blogs, back_populates='blogs')    

    def __str__(self):
        return f'<[Blog: {self.title}] by: {self.author.emails[0].email}>'

    def get_json(self, exclude=None):
        json_obj = super().get_json(exclude=exclude)
        json_obj['comments'] = [
                comment.get_json(
                    exclude=['blog']
                ) for comment in self.comments
        ] 
        return json_obj
