from flask import current_app, request, jsonify, url_for
from flask.views import MethodView

class BaseView(MethodView):

    model = None
    context = None
    form = None
    object_context_name = 'object'
    object_id_kwarg = 'obj_id'

    def get_model(self):
        return self.model

    def get_context(self, **kwargs):
        self.context = kwargs
        return self.context

    def get_form(self):
        return self.form

    def get_object_context_name(self):
        return self.object_context_name

    def get_object_id_kwarg(self):
        return self.object_id_kwarg

    def create_form(self, **kwargs):
        return self.get_form(**kwargs)

    def dispatch_request(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return super().dispatch_request(*args, **kwargs)

    def get(self, *args, **kwargs):
        context = self.get_context(**kwargs)
        return jsonify(**context)

    def get_json(self, obj, *args, **kwargs):
        return obj.get_json(*args, **kwargs)


class SingleObjectView(BaseView):

    default_query = None 

    def get_default_query(self):
        return (
            model.query(model).filter(obj_id).one() 
            if self.default_query is None 
            else self.default_query
        )

    def get(self, *args, **kwargs):
        obj_id = kwargs.get(self.get_object_id_kwarg)
        model = self.get_model()
        obj = self.get_default_query()
        return super().get(**{self.get_object_context_name(): self.get_json(obj)})


class ListObjectView(BaseView):
    object_context_name = 'objects'

    def get_default_query(self):
        return self.model.query(self.model).all()

    def get(self, *args, **kwargs):
        model = self.get_model()

        objects = [self.get_json(obj) for obj in self.get_default_query()]
        return super().get(**{self.get_object_context_name():objects})

