from betahaus.pyracont import BaseFolder

from progress import ProgressMF as _


class Tasks(BaseFolder):
    """ Container for tasks. """
    allowed_contexts = () #Not manually addable
    content_type = 'Tasks'
    display_name = _(u"Tasks")
    custom_accessors = {'title':'get_title'}
    
    def get_title(self, default=''):
        return self.display_name
    