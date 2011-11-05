from pyramid.threadlocal import get_current_request
from betahaus.pyracont.interfaces import IContentFactory


def get_addable_content(context, request=None):
    if request is None:
        request = get_current_request()
    results = []
    for (name, factory) in request.registry.getUtilitiesFor(IContentFactory):
        if not context.content_type in factory._callable.allowed_contexts:
            continue
        #FIXME: Check add permissions here
        results.append((name, factory.title))
    return tuple(results)
