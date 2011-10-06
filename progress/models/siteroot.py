from progress.models.base import BaseFolder
from progress.models.factories import content_factory


@content_factory('SiteRoot')
class SiteRoot(BaseFolder):
    """ Root for the site. """
    schemas = {'edit': 'site_root'}
    allowed_contexts = ()
    content_type = 'SiteRoot'
