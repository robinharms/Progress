from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory


@content_factory('Users')
class Users(BaseFolder):
    """ Container for users. """
    allowed_contexts = () #Not manually addable
    content_type = 'Users'