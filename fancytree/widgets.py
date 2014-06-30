from itertools import chain

from django import forms
from django.conf import settings
from django.forms.widgets import Widget
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDict, MergeDict

try:
    import simplejson as json
except ImportError:
    import json

def get_doc(node, values):
    if hasattr(node, "get_doc"):
        return node.get_doc(values)
    if hasattr(node, "name"):
        name = node.name
    else:
        name = unicode(node)
    doc = {"title": name, "key": node.pk, "url": node.url}
    if str(node.pk) in values:
        doc['select'] = True
        doc['expand'] = True
    return doc

def get_tree(nodes, values):
    parent = {}
    parent_level = 0
    stack = []
    results = []

    def find_parent(child, results):
        for node in reversed(results):
            if child.url.startswith(node["url"]):
                if child.parent_id != node["key"]:
                    return find_parent(child, node["children"])
                else:
                    return node

    def add_doc(node):
        if node.level == 0:
            results.append(get_doc(node, values))
        elif node.level >= 1:
            parent = find_parent(node, results)
            children = parent.get("children", [])
            child = get_doc(node, values)
            if child.get('select', False):
                parent['expand'] = True
            children.append(child)
            parent["children"] = children
            parent["folder"] = True

    if not nodes:
        return results

    for node in nodes:
        add_doc(node)

    return results


class FancyTreeWidget(Widget):
    def __init__(self, attrs=None, choices=(), queryset=None, select_mode=2):
        super(FancyTreeWidget, self).__init__(attrs)
        self.queryset = queryset
        self.select_mode = select_mode
        self.choices = list(choices)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        if has_id:
            output = [u'<div id="%s"></div>' % attrs['id']]
            id_attr = u' id="%s_checkboxes"' % (attrs['id'])
        else:
            output = [u'<div></div>']
            id_attr = u''
        output.append(u'<ul class="fancytree_checkboxes"%s>' % id_attr)
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], option_value))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(
                u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label)
            )
        output.append(u'</ul>')
        output.append(u'<script type="text/javascript">')
        if has_id:
            output.append(u'var fancytree_data_%s = %s;' % (
                attrs['id'],
                json.dumps(get_tree(self.queryset, str_values))
            ))
            output.append(
                """
                $(".fancytree_checkboxes").hide();
                $(function() {
                    $("#%(id)s").fancytree({
                        checkbox: true,
                        selectMode: %(select_mode)d,
                        source: fancytree_data_%(id)s,
                        debugLevel: %(debug)d,
                        select: function(event, data) {
                            $('#%(id)s_checkboxes').find('input[type=checkbox]').removeProp('checked');
                            var selNodes = data.tree.getSelectedNodes(%(select_mode)d === 3);
                            var selKeys = $.map(selNodes, function(node){
                                   $('#%(id)s_' + (node.key)).prop('checked', 'checked');
                                   return node.key;
                            });
                        },
                        click: function(event, data) {
                            var node = data.node;
                            if (event.targetType == "fancytreeclick")
                                node.toggleSelected();
                        },
                        keydown: function(event, data) {
                            var node = data.node;
                            if (event.which == 32) {
                                node.toggleSelected();
                                return false;
                            }
                        }
                    });
                });
                """ % {
                    'id': attrs['id'],
                    'debug': settings.DEBUG and 1 or 0,
                    'select_mode': self.select_mode,
                }
            );
        output.append(u'</script>')
        return mark_safe(u'\n'.join(output))

    class Media:
        css = {
            'all': ('fancytree/skin-vista/ui.fancytree.css',)
        }
        js = (
            'fancytree/jquery.fancytree.min.js',
        )
