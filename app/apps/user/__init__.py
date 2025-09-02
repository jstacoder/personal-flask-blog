from flask import Blueprint, jsonify, request
from flask.views import MethodView

from ...models.user import User

UserBlueprint = Blueprint("user", __name__)

class GetUserByIdView(MethodView):
    def get(self, user_id=None):
        user = User.query(User).session.get(User, user_id)
        if user is None:
            return jsonify({"success": False, "error": "user not found"}), 404
        return jsonify({
            'id':user.id,
            'username':user.username
        }), 200


class GetUsersView(MethodView):
    def get(self):
        users = User.query(User).all()
        rtn = []
        data = ({
            'id':user.id,
            'username':user.username
        } for user in users)
        while True:
            try:
                curr = next(data)
                rtn.append(curr)
            except StopIteration:
                break
        return jsonify(rtn)


class CreateEditUserView(MethodView):
    def post(self):
        user = User()
        user.username = request.json.get("username")
        user.save()
        return jsonify({"success":True}), 201

    def put(self, user_id):
        user = User.query(User).session.get(User, user_id)
        if user is None:
            return jsonify({"success":False, "error":"user not found"}), 404
        user.username = request.json.get("username")
        user.save()
        return jsonify({"success":True}), 201

    def delete(self, user_id):
        user = User.query(User).session.get(User, user_id)
        if user is None:
            return jsonify({"success":False, "error":"user not found"}), 404
        user.query(User).session.remove(user)
        user.query(User).session.commit()
        return jsonify({"success":True}), 201
        


UserBlueprint.add_url_rule(
        "/", view_func=GetUsersView.as_view(name="get_users")
)
UserBlueprint.add_url_rule(
        "/", view_func=CreateEditUserView.as_view(name="create_user")
)
UserBlueprint.add_url_rule(
        "/<user_id>/", view_func=CreateEditUserView.as_view(name="edit_user")
)
UserBlueprint.add_url_rule(
        "/<user_id>/", view_func=GetUserByIdView.as_view(name="user_by_id")
)
