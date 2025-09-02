import sqlalchemy as sa
from sqlalchemy import Table

from .base import Base

tag_blogs = Table(
    "tag_blogs",
    Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('tag_id', sa.ForeignKey('tags.id')),
    sa.Column('blog_id', sa.ForeignKey('blogs.id')),
)

tag_pages = Table(
   "tag_pages",
   Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('tag_id', sa.ForeignKey('tags.id')),
    sa.Column('page_id', sa.ForeignKey('pages.id')),    
)
