import colander
import deform

from progress.models.factories import schema_factory
from progress import ProgressMF as _


def _first_name():
    return colander.SchemaNode(colander.String(),
                               title = _(u"First name"),
                               missing=u"",)

def _last_name():
    return colander.SchemaNode(colander.String(),
                               title = _(u"Last name"),
                               missing=u"",)

def _password():
    return colander.SchemaNode(colander.String(),
                               validator=colander.Length(min=5),
                               widget=deform.widget.CheckedPasswordWidget(),)

def _userid():
    return colander.SchemaNode(colander.String(),)

def _email():
    return colander.SchemaNode(colander.String(),
                               validator=colander.Email(),)


@schema_factory('add_user')
class AddUserSchema(colander.Schema):
    userid = _userid()
    email = _email()
    first_name = _first_name()
    last_name = _last_name()
    password = _password()


@schema_factory('edit_user')
class EditUserSchema(colander.Schema):
    email = _email()
    first_name = _first_name()
    last_name = _last_name()

