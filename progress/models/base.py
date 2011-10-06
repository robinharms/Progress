from uuid import uuid4

from repoze.folder import Folder
from BTrees.OOBTree import OOBTree
from zope.interface import implements
from zope.component.event import objectEventNotify
from slugify import slugify

from progress.models.datetime_helpers import utcnow
from progress.models.interfaces import IBaseFolder
from progress.events import ObjectUpdatedEvent
from progress.models.factories import createContent


def generate_slug(parent, text, limit=20):
    """ Suggest a name for content that will be added.
        text is a title or similar to be used.
    """
    suggestion = slugify(text[:limit])
    
    #Is the suggested ID already unique?
    if suggestion not in parent:
        return suggestion
    
    #ID isn't unique, let's try to generate a unique one.
    RETRY = 100
    i = 1
    while i <= RETRY:
        new_s = "%s-%s" % (suggestion, str(i))
        if new_s not in parent:
            return new_s
        i += 1
    #If no id was found, don't just continue
    raise KeyError("No unique id could be found")


class BaseFolder(Folder):
    """ Base class for most content. """
    implements(IBaseFolder)
    schemas = {}
    content_type = 'BaseFolder'
    allowed_contexts = ()
    custom_accessors = {}
    custom_mutators = {}
    versioning_fields = ()

    def __init__(self, data=None, **kwargs):
        super(BaseFolder, self).__init__(data=data)
        self.set_field_value('created', utcnow())
        self.set_field_value('modified', utcnow())
        self.set_field_value('uid', uuid4())
        self.set_field_appstruct(kwargs, notify=False)

    @property
    def title(self):
        return self.get_field_value('title', '')

    @property
    def created(self):
        return self.get_field_value('created')

    @property
    def modified(self):
        return self.get_field_value('modified')

    @property
    def uid(self):
        return self.get_field_value('uid')

    @property
    def _field_storage(self):
        if not hasattr(self, '__field_storage__'):
            self.__field_storage__ = OOBTree()
        return self.__field_storage__

    def suggest_name(self, parent):
        """ Suggest a name if this content would be added to parent.
        """
        return generate_slug(parent, self.title)

    def mark_modified(self):
        """ Mark content as modified. """
        self._field_storage['modified'] = utcnow()

    def get_field_value(self, key, default=None):
        """ Return field value, or default """
        if key in self.custom_accessors:
            return getattr(self, self.custom_accessors[key])(default=default)
        if key in self.versioning_fields:
            return self._get_versioning_field_value(key, default=default)
        return self._field_storage.get(key, default)
    
    def set_field_value(self, key, value):
        """ Set field value.
            Will not send events, so use this if you silently want to change a single field.
            You can override field behaviour by either setting custom mutators
            or make a field a versioning field.
        """
        if key in self.custom_mutators:
            mutator = self.custom_mutators[key]
            mutator(value)
            return
        if key in self.versioning_fields:
            self._set_versioning_field_value(key, value)
            return
        self._field_storage[key] = value

    def _get_versioning_field_value(self, key, default=None):
        field = self._versioning_field(key)
        value = field.get_last_revision_value(default=default)
        if value == default:
            return default
        return value

    def _set_versioning_field_value(self, key, value):
        field = self._versioning_field(key)
        field.add(value)

    def _versioning_field(self, key):
        if not key in self._field_storage:
            self._field_storage[key] = createContent('VersioningField')
        return self._field_storage[key]

    def get_field_appstruct(self, schema):
        """ Return a dict of all fields and their values.
            Deform expects input like this when rendering already saved values.
        """
        marker = object()
        appstruct = {}
        for field in schema:
            value = self.get_field_value(field.name, marker)
            if value != marker:
                appstruct[field.name] = value
        return appstruct

    def set_field_appstruct(self, values, notify=True, mark_modified=True):
        """ Set values from a dict or similar key/value object.
            Only updates if the new value isn't the same as the old one.
            Returns set of keys (fieldnames) that have been updated.
        """
        updated = set()
        for (k, v) in values.items():
            cur = self.get_field_value(k)
            if cur == v:
                continue
            self.set_field_value(k, v)
            updated.add(k)
        if updated:
            if notify:
                objectEventNotify(ObjectUpdatedEvent(self, fields=updated))
            if mark_modified:
                self.mark_modified()
        return updated
