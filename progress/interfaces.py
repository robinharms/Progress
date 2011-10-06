from zope.interface import Interface
from zope.interface import Attribute

#Event interfaces
class IObjectUpdatedEvent(Interface):
    """ An object event for object updated.
        fields can be set to indicate that only a few fields were updated.
    """
    object = Attribute("Object this event is for")
    fields = Attribute("List of fields that were updated.")
    
    def __init__(object, fields=(), metadata=True):
        """ Create event. """
        