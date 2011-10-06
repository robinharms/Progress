import colander
from betahaus.pyracont.decorators import schema_factory


@schema_factory('site_root')
class SiteRootSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                )
