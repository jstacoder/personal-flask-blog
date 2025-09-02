from flask import request
from flask.views import MethodView

class IndexView(MethodView):
    def get(self):
        return "helllo from flask"

class NameView(MethodView):
    def get(self, name):
        return f'hello {name}'
