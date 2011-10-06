import venusian
from zope.component.factory import Factory
from zope.component import getUtility

from progress.models.interfaces import IContentFactory
from progress.models.interfaces import ISchemaFactory


class content_factory(object):
    """ Decorator for factories"""
    venusian = venusian
    
    def __init__(self, factory_name):
        self.factory_name = factory_name

    def register(self, scanner, name, wrapped):
        factory = Factory(wrapped, self.factory_name)
        scanner.config.registry.registerUtility(factory, IContentFactory, self.factory_name)

    def __call__(self, wrapped):
        self.venusian.attach(wrapped, self.register, category='pyramid')
        return wrapped


class schema_factory(content_factory):
    def register(self, scanner, name, wrapped):
        factory = Factory(wrapped, self.factory_name)
        scanner.config.registry.registerUtility(factory, ISchemaFactory, self.factory_name)


def createSchema(factory_name, context, request, **kwargs):
    """ Create a colander schema object.
        context, request and kwargs are for bind, which occurs
        after object construction. Hence this factory works a bit
        different than the standard one.
        See the colander documentation for information on schema bind.
    """
    schema = getUtility(ISchemaFactory, factory_name)()
    schema.bind(context=context,
                request=request,
                **kwargs)
    return schema


def createContent(factory_name, *args, **kwargs):
    """ Works almost the same as createObject.
    """
    return getUtility(IContentFactory, factory_name)(*args, **kwargs)

