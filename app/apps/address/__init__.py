from flask import Blueprint

from ...models.email_address import EmailAddress
from ...views.generic import ListObjectView, SingleObjectView


EmailBlueprint = Blueprint('emails', __name__)

class GetEmailView(SingleObjectView):
    model = EmailAddress
    context_object_name = 'email'
    object_id_kwarg = 'email_id'


class GetEmailsView(ListObjectView):
    model = EmailAddress
    context_object_name = 'emails'



EmailBlueprint.add_url_rule('/', view_func=GetEmailsView.as_view('get_emails'))
EmailBlueprint.add_url_rule('/<email_id>/', view_func=GetEmailView.as_view('get_email'))

