from typing import List

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base as BaseModel
from .joins import tag_blogs, tag_pages
from .shared import GenericForeignKeyModel


class Tag(GenericForeignKeyModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(sa.String(255))

    #tag_pages_id = mapped_column(ForeignKey('tag_pages.id'))
    #tag_blogs_id = mapped_column(ForeignKey('tag_blogs.id', name='tag_blogs_idfk'))

    def __repr__(self):
        return self.value
