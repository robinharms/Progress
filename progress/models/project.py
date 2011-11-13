from zope.interface import implements
from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory
from betahaus.pyracont.factories import createContent

from progress import ProgressMF as _
from progress.models.interfaces import IProject


@content_factory('Project')
class Project(BaseFolder):
    """ User model. """
    schemas = {'edit': 'project', 'add': 'project'}
    content_type = 'Project'
    display_name = _(u"Project")
    allowed_contexts = ('SiteRoot',)
    implements(IProject)
    #add_permission = security.ADD_USER

    def __init__(self, data=None, **kwargs):
        super(Project, self).__init__(data=data, **kwargs)
        self['tasks'] = createContent('Tasks')