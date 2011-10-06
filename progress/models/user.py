from hashlib import sha1

from zope.interface import implements
from repoze.folder import unicodify
from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory


def get_sha_password(password):
    """ Encode a plaintext password to sha1. """
    if isinstance(password, unicode):
        password = password.encode('UTF-8')
    return 'SHA1:' + sha1(password).hexdigest()


@content_factory('User')
class User(BaseFolder):
    """ User model. """
    #implements(IUser)
    schemas = {'edit': 'edit_user', 'add': 'add_user'}
    content_type = 'User'
    #display_name = _(u"User")
    allowed_contexts = ('Users',)
    #add_permission = security.ADD_USER
    custom_mutators = {'password':'set_password'}

    def suggest_name(self, parent):
        """ Suggest a name if this content would be added to parent.
            This is a "hacky" version since userid will be set, but should be removed.
        """
        userid = self.get_field_value('userid', None)
        assert userid is not None
        assert userid not in parent
        del self._field_storage['userid']
        return userid
    
    def set_password(self, value):
        """ Encrypt a plaintext password. """
        if not isinstance(value, unicode):
            value = unicodify(value)
        if len(value) < 5:
            raise ValueError("Password must be longer than 4 chars")
        value = get_sha_password(value)
        self.set_field_value('password', value)

    @property
    def title(self):
        out = "%s %s" % ( self.get_field_value('first_name'), self.get_field_value('last_name') )
        return out.strip()
