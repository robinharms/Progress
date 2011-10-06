from datetime import datetime

from persistent import Persistent
from BTrees.LOBTree import LOBTree
from pyramid.threadlocal import get_current_request
from pyramid.security import authenticated_userid

from progress.models.datetime_helpers import utcnow
from progress.models.factories import content_factory


@content_factory('VersioningField')
class VersioningField(Persistent):
    """ Field that has versioning rather than just storing one value. """

    def __init__(self):
        self.__revision_values__ = LOBTree()
        self.__revision_authors__ = LOBTree()
        self.__revision_created_timestamps__ = LOBTree()

    @property
    def _revision_values(self):
        return self.__revision_values__
    
    @property
    def _revision_authors(self):
        return self.__revision_authors__

    @property
    def _revision_created_timestamps(self):
        return self.__revision_created_timestamps__

    def get_current_rev(self):
        if len(self._revision_values) == 0:
            return 0
        self._revision_values.maxKey()

    def add(self, value, author=None, created=None):
        if created is None:
            created = utcnow()
        assert isinstance(created, datetime)
        if author is None:
            request = get_current_request()
            author = authenticated_userid(request)
        #author might still be None, if this is run by a script or by an unauthenticated user
        id = self.get_current_rev()+1
        self._revision_values[id] = value
        self._revision_authors[id] = author
        self._revision_created_timestamps[id] = created
    
    def remove(self, id):
        del self._revision_values[id]
        del self._revision_authors[id]
        del self._revision_created_timestamps[id]

    def get_last_revision(self, default=None):
        if not len(self._revision_values):
            return default
        id = self.get_current_rev()
        result = {}
        result['value'] = self._revision_values[id]
        result['author'] = self._revision_authors[id]
        result['created'] = self._revision_created_timestamps[id]
        return result

    def get_last_revision_value(self, default=None):
        if not len(self._revision_values):
            return default
        id = self.get_current_rev()
        return self._revision_values[id]

    def __len__(self):
        return len(self._revision_values)
