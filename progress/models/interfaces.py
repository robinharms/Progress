from zope.interface import Attribute
from zope.interface import Interface
from betahaus.pyracont.interfaces import IBaseFolder


class IIteration(IBaseFolder):
    """ Iteration """


class ITask(IBaseFolder):
    """ Task content type """


class ITasks(IBaseFolder):
    """ Tasks content type - a container for tasks. Always present in projects. """


class IProject(IBaseFolder):
    """ Project content type """
