import colander
from deform.widget import TextAreaWidget
from deform.widget import SelectWidget
from betahaus.pyracont.decorators import schema_factory

from progress import ProgressMF as _


@colander.deferred
def deferred_state_widget(node, kw):
    #FIXME: Custom state values
    values = ((u"unassigned", _(u"Unassigned")),
              (u"ongoing", _(u"Ongoing")),
              (u"completed", _(u"Completed")),
               )
    return SelectWidget(values=values)


@schema_factory('task')
class TaskSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                )
    text = colander.SchemaNode(colander.String(),
                               widget=TextAreaWidget(rows=10, cols=60),
                               missing=u"",)
    estimated_time = colander.SchemaNode(colander.Integer(),
                                         title = _(u"Expected time, in hours."),
                                         missing=colander.null,)
    state = colander.SchemaNode(colander.String(),
                                widget=deferred_state_widget,
                                default=u'unassigned',
                                )