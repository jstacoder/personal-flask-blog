from sqlalchemy.ext.hybrid import hybrid_property
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from inflection import singularize, camelize, underscore
from importlib import import_module

from .base import session, Base as BaseModel

class Status(Enum):
    published = "published"
    draft = "draft"
    deleted = "deleted"


class GenericForeignKeyModel(BaseModel):
    __abstract__ = True

    _related_model = None

    content_type: Mapped[str] = mapped_column(sa.String(255))
    object_id: Mapped[int] = mapped_column(sa.Integer)

    @hybrid_property
    def content_object(self):
        model_class_name = singularize(
                camelize(
                    self.content_type
                )
        )
        model_module_name = underscore(model_class_name)
        model_module = import_module(f'models.{model_module_name}')
        model_class = getattr(model_module, model_class_name, None)
        if model_class is None:
            raise TypeError(
                    f'models.{model_module_name} has no class '
                    f'named {model_class_name}'
            )
        return model_class.query.get(self.object_id)

    def add_model_instance(self, model_instance):
        if not hasattr(model_instance, 'id'):
            model_instance.save()
        self.object_id = model_instance.id
        self.content_type = model_instance.__class__.__tablename__

        session.add(self)
        session.commit()
        return self

    def load_related_model(self):
        pass



