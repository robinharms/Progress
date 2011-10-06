from zope.interface import implements

from progress.models.base import BaseFolder
from progress.models.factories import content_factory
from progress.models.factories import createContent
from progress import ProgressMF as _


@content_factory('Project')
class Project(BaseFolder):
    """ User model. """
    schemas = {'edit': 'project', 'add': 'project'}
    content_type = 'Project'
    display_name = _(u"Project")
    allowed_contexts = ('SiteRoot',)
    #add_permission = security.ADD_USER

    def __init__(self, data=None, **kwargs):
        supet(Project, self).__init__(data=data, **kwargs)
        self['tasks'] = createContent('Tasks')
