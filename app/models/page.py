import datetime as dt
from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import functions

from .base import Base as BaseModel
from .shared import Status
#from models.joins import tag_pages


class Page(BaseModel):

    id:Mapped[int] = mapped_column(
            sa.Integer,
            primary_key=True
    )

    title:Mapped[str] = mapped_column(sa.String(255))
    content:Mapped[str] = mapped_column(sa.Text)
    slug:Mapped[str] = mapped_column(sa.String(255))

    date_added:Mapped[dt.datetime] = mapped_column(
            sa.DateTime,
            default=functions.now()   
    )
    
    status: Mapped[Status] = mapped_column(
            sa.Enum(Status), 
            default="draft"
    )
    blog_id: Mapped[int] = mapped_column(sa.ForeignKey('blogs.id'), nullable=True)
    blog: Mapped['Blog'] = relationship('Blog', back_populates='pages')
    #tags: Mapped[List["Tag"]] = relationship(
    #        "Tag",
    #        secondary=tag_pages, 
    #        back_populates='pages'
    #)    
