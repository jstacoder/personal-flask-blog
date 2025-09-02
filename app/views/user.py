from flask.views import MethodView
from models.user import User

class UserApiView(MethodView):
     model = User


