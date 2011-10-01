from pyramid.view import view_config
from progress.models import MyModel

@view_config(context=MyModel, renderer='progress:templates/mytemplate.pt')
def my_view(request):
    return {'project':'Progress'}
