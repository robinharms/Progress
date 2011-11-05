from pyramid.decorator import reify
from pyramid.security import authenticated_userid
from pyramid.traversal import find_root
from pyramid.renderers import get_renderer
from pyramid.renderers import render
from pyramid.url import resource_url

from progress import ProgressMF as _
from pyramid.location import lineage


class BaseView(object):
    """ Base view """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.response = dict(
            api = self,
            form_resources = {},
            main_tpl_macro = get_renderer('templates/main.pt').implementation().macros['master'],
            resource_url = resource_url,
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

    def render_context_menu(self):
        response = {}
        actions = []
        context_url = resource_url(self.context, self.request)
        if 'edit' in self.context.schemas:
            actions.append({'id':'edit', 'title':_(u"Edit"), 'url': "%sedit" % context_url})
            #FIXME: Check edit perm too
        response['actions'] = actions
        return render('templates/snippets/context_menu.pt', response, request=self.request)

    def render_pathbar(self):
        response = {}
        response['resource_url'] = resource_url
        path = list(lineage(self.context))
        path.reverse()
        response['path'] = tuple(path)
        return render('templates/snippets/pathbar.pt', response, request=self.request)
