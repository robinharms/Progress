import colander

from progress.models.factories import schema_factory


@schema_factory('site_root')
class SiteRootSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                )
