from unittest import TestCase

from pyramid import testing
from betahaus.pyracont.interfaces import IContentFactory
from zope.component.factory import Factory


class DummyContext(testing.DummyResource):
    allowed_contexts = ['DummyContext']
    content_type = 'DummyContext'


class UtilsTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _register_dummy_factory(self):
        from betahaus.pyracont.interfaces import IContentFactory
        factory = Factory(DummyContext, 'DummyContext')
        self.config.registry.registerUtility(factory, IContentFactory, 'DummyContext')

    def test_get_addable_content(self):
        self._register_dummy_factory()
        
        #self.config.scan('progress')
        from progress.utils import get_addable_content
        request = testing.DummyRequest()
        context = DummyContext()

        res = get_addable_content(context, request)
        #List with display name, id
        self.assertEqual(((u'DummyContext', 'DummyContext'),), res)