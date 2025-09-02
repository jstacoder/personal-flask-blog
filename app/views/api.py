from flask.views import MethodView
from flask import render_template

class BaseApiView(MethodView):
    model = None
    template = None

    def get(self, id=None):
        if id is None:
            return self.get_list()
        model_instance = self.model.query(id=id).get()
        return self.render(template="api/get.html",object=model_instance)

    def get_list(self):
        obj_list = self.model.query.all()
        return self.render(template="api/get_list.html", obj_list=obj_list)

    def render(self, template=None, **kwargs):
        context = self.get_context(**kwargs)
        return render_template(template, context)
