import colander

from progress.models.factories import schema_factory


@schema_factory('project')
class ProjectSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                )
