import colander
from betahaus.pyracont.decorators import schema_factory


@schema_factory('iteration')
class IterationSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                )
    