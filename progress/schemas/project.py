import colander
from betahaus.pyracont.decorators import schema_factory


@schema_factory('project')
class ProjectSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                )
