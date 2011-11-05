from pyramid.config import Configurator
from repoze.zodbconn.finder import PersistentApplicationFinder
from pyramid.i18n import TranslationStringFactory
from pyramid.session import UnencryptedCookieSessionFactoryConfig


ProgressMF = TranslationStringFactory('Progress')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """    
    from progress.models.app import appmaker
    from progress.security import authn_policy
    from progress.security import authz_policy
    
    zodb_uri = settings.get('zodb_uri', False)
    if zodb_uri is False:
        raise ValueError("No 'zodb_uri' in application configuration.")

    finder = PersistentApplicationFinder(zodb_uri, appmaker)
    def get_root(request):
        return finder(request.environ)

    sessionfact = UnencryptedCookieSessionFactoryConfig('messages')
    
    config = Configurator(settings=settings,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy,
                          root_factory=get_root,
                          session_factory = sessionfact,)
    
    config.add_static_view('static', 'progress:static')
    config.add_static_view('deform', 'deform:static')

    #Set which mailer to use
    #config.include(settings['mailer'])
    
    config.add_translation_dirs('deform:locale/',
                                'colander:locale/',
                                #'progress:locale/',
                                )


    config.hook_zca()
    config.scan('progress')
    config.scan('betahaus.pyracont.fields.versioning')
    return config.make_wsgi_app()


