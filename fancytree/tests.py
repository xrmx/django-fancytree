from django.test import TestCase
from fancytree.widgets import FancyTreeWidget

class WidgetTest(TestCase):
    def test_widget_loads(self):
        widget = FancyTreeWidget()
        self.assertIsInstance(widget, FancyTreeWidget)

    def test_widget_render_js(self):
        widget = FancyTreeWidget()
        attrs = {'id': 'fancyfoo'}
        html = widget.render("foo", ["1", "2"], attrs)
        self.assertTrue('.fancytree({' in html)
        self.assertTrue('<ul class="fancytree_checkboxes" id="fancyfoo_checkboxes">' in html)

    def test_widget_render_single_value(self):
        widget = FancyTreeWidget()
        attrs = {'id': 'fancyfoo'}
        html = widget.render("foo", "1", attrs)
        self.assertTrue('.fancytree({' in html)
