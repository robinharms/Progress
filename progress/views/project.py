from pyramid.view import view_config

from progress.views.base import BaseView
from progress.models.interfaces import IProject

class ProjectView(BaseView):
    
    @view_config(context = IProject, renderer = 'templates/project_view.pt')
    def project_view(self):
        return self.response
