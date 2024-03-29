import colander
from deform.form import Form
from deform.exception import ValidationFailure
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.url import resource_url
from betahaus.pyracont.interfaces import IBaseFolder
from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.factories import createContent

from progress.views.base import BaseView


BASE_EDIT_TPL = "templates/edit.pt"
BASE_VIEW_TPL = "templates/view.pt"


class CRUDView(BaseView):

    @view_config(name="add", context=IBaseFolder, renderer=BASE_EDIT_TPL)
    def add(self):
        if 'cancel' in self.request.POST:
            url = resource_url(self.context, self.request)
            return HTTPFound(location=url)

        type = self.request.GET['type']
        obj = createContent(type)
        schema = createSchema(obj.schemas['add']).bind(context = self.context, request = self.request)
        form = Form(schema, buttons=('save', 'cancel',))
        self.register_form_resources(form)

        if 'save' in self.request.POST:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            
            obj.set_field_appstruct(appstruct)
            name = obj.suggest_name(self.context)
            self.context[name] = obj

            url = resource_url(self.context, self.request)
            return HTTPFound(location=url)

        self.response['form'] = form.render()
        return self.response

    @view_config(name="edit", context=IBaseFolder, renderer=BASE_EDIT_TPL)
    def edit(self):
        if 'cancel' in self.request.POST:
            url = resource_url(self.context, self.request)
            return HTTPFound(location=url)

        schema = createSchema(self.context.schemas['edit']).bind(context = self.context, request = self.request)
        form = Form(schema, buttons=('save', 'cancel',))
        self.register_form_resources(form)

        if 'save' in self.request.POST:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            self.context.set_field_appstruct(appstruct)
            url = resource_url(self.context, self.request)
            return HTTPFound(location=url)

        appstruct = self.context.get_field_appstruct(schema)
        self.response['form'] = form.render(appstruct=appstruct)
        return self.response

    @view_config(name="delete", context=IBaseFolder, renderer=BASE_EDIT_TPL)
    def delete(self):
        return self.response

    @view_config(context=IBaseFolder, renderer=BASE_VIEW_TPL)
    def view(self):
        return self.response
