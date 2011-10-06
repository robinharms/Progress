from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory


@content_factory('SiteRoot')
class SiteRoot(BaseFolder):
    """ Root for the site. """
    schemas = {'edit': 'site_root'}
    allowed_contexts = ()
    content_type = 'SiteRoot'
