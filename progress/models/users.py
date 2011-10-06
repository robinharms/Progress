from progress.models.base import BaseFolder
from progress.models.factories import content_factory


@content_factory('Users')
class Users(BaseFolder):
    """ Container for users. """
    allowed_contexts = () #Not manually addable
    content_type = 'Users'