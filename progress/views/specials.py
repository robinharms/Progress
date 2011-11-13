from pyramid.url import resource_url
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from progress.models.interfaces import ITasks


@view_config(context = ITasks)
def redirect_to_parent(context, request):
    """ Redurect to parent view. Must not be registered for root """
    parent = context.__parent__
    url = resource_url(parent, request)
    return HTTPFound(location = url)
