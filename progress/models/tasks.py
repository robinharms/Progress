from betahaus.pyracont import BaseFolder
from BTrees.LOBTree import LOBTree
from betahaus.pyracont.decorators import content_factory
from zope.interface import implements

from progress import ProgressMF as _
from progress.models.interfaces import ITasks


@content_factory('Tasks')
class Tasks(BaseFolder):
    """ Container for tasks. """
    implements(ITasks)
    allowed_contexts = () #Not manually addable
    content_type = 'Tasks'
    display_name = _(u"Tasks")
    custom_accessors = {'title':'get_title'}
    

    def __init__(self, data=None, **kwargs):
        super(Tasks, self).__init__(data=data, **kwargs)
        self.__task_ids__ = LOBTree()

    def get_title(self, default='', key=None):
        return self.display_name
    
    def mark_task_id(self):
        if len(self.__task_ids__) == 0:
            id = 1 #Start at 1
        else:
            id = self.__task_ids__.maxKey()+1

        suggest_name = unicode(id)
        self.add_task_id(id, suggest_name)
        return suggest_name
    
    def add_task_id(self, id, value):
        if id in self.__task_ids__:
            raise ValueError("id %s already exist in %s" % (id, self))
        self.__task_ids__[id] = value
