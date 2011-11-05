from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory
from zope.interface import implements

from progress import ProgressMF as _
from progress.models.interfaces import ITask


@content_factory('Task')
class Task(BaseFolder):
    """ Container for tasks. """
    implements(ITask)
    allowed_contexts = ('Tasks')
    content_type = 'Task'
    display_name = _(u"Task")
    schemas = {'add':'task', 'edit':'task'}
    custom_fields = {'text': 'VersioningField',
                     'state': 'VersioningField',}

    def suggest_name(self, parent):
        """ Suggest a name if this content would be added to parent.
            Task content types are only addable to a Tasks folder,
            and those have a method for checking next free task id.
        """
        return parent.mark_task_id()