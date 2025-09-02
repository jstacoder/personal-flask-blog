import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apiflask import Schema
from apiflask.fields import Integer, String

from .base import Base as BaseModel


class EmailInput(Schema):
    email = String()
    user_id = Integer()


class EmailAddress(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True)
    is_primary: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    user_id = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="emails")

    def __repr__(self):
        return self.email   
