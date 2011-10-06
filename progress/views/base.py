from pyramid.decorator import reify
from pyramid.security import authenticated_userid
from pyramid.traversal import find_root
from pyramid.renderers import get_renderer


class BaseView(object):
    """ Base view """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.response = dict(
            api = self,
            form_resources = {},
            main_tpl_macro = get_renderer('templates/main.pt').implementation().macros['master']
        )
    
    @reify
    def userid(self):
        return authenticated_userid(self.request)
    
    @reify
    def root(self):
        return find_root(self.context)
    
    @reify
    def user(self):
        return self.root['users'].get(self.userid)

    def register_form_resources(self, form):
        """ Append form resources if they don't already exist in response['form_resources'] """
        res = self.response['form_resources']
        for (k, v) in form.get_widget_resources().items():
            if k not in res:
                res[k] = set()
            res[k].update(v)
