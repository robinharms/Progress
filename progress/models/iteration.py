from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory
from zope.interface import implements

from progress import ProgressMF as _
from progress.models.interfaces import IIteration


@content_factory('Iteration')
class Iteration(BaseFolder):
    """ Iteration. """
    implements(IIteration)
    allowed_contexts = ('Project')
    content_type = 'Iteration'
    display_name = _(u"Iteration")
    schemas = {'add':'iteration', 'edit':'iteration'}
