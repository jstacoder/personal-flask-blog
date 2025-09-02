from flask_security import Security, current_user, auth_required, hash_password,SQLAlchemySessionUserDatastore, permissions_accepted

from .models.base import session as db_session
from .models.user import User, AnonymousUser, Role

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(user_datastore)

#login_manager.anonymous_user = AnonymousUser

#@login_manager.user_loader
#def load_user(user_id):
#    return User.query(User).filter_by(User.auth_info.id==user_id).first()


