from itertools import chain

from django import forms
from django.conf import settings
from django.forms.widgets import Widget
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDict, MergeDict
from mptt.templatetags.mptt_tags import cache_tree_children
from mptt.forms import TreeNodeChoiceField

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
    doc = {"title": name, "key": node.pk}
    if str(node.pk) in values:
        doc['selected'] = True
        doc['expand'] = True
    return doc

def recursive_node_to_dict(node, values, hide_folder_checkbox):
    result = get_doc(node, values)
    children = [recursive_node_to_dict(c, values, hide_folder_checkbox) for c in node.get_children()]
    if children:
        expand = [c for c in children if c.get('selected', False)]
        if expand:
            result["expand"] = True
        result["folder"] = True
        if hide_folder_checkbox:
            result['hideCheckbox'] = True
        result['children'] = children
    return result

def get_tree(nodes, values, hide_folder_checkbox):
    root_nodes = cache_tree_children(nodes)
    return [recursive_node_to_dict(n, values, hide_folder_checkbox) for n in root_nodes]

class FancyTreeWidget(Widget):
    def __init__(self, attrs=None, choices=(), queryset=None, select_mode=2, hide_folder_checkbox=False):
        super(FancyTreeWidget, self).__init__(attrs)
        self.queryset = queryset
        self.select_mode = select_mode
        self.choices = list(choices)
        self.hide_folder_checkbox = hide_folder_checkbox

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        if not isinstance(value, (list, tuple)):
            value = [value]
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        if has_id:
            output = [u'<div id="f%s"></div>' % attrs['id']]
            id_attr = u' id="%s_checkboxes"' % (attrs['id'])
        else:
            output = [u'<div></div>']
            id_attr = u''
#        output.append(u'<ul class="fancytree_checkboxes"%s>' % id_attr)
        if self.select_mode == 3:
            multiple_tag = u'multiple'
        else:
            multiple_tag = u''
        output.append(u'<select id="%s" name="%s" class="fancytree_checkboxes"%s %s>' % (attrs['id'], name, id_attr, multiple_tag))
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], option_value))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            # cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
       #     rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
       #     output.append(
        #        u'<label%s>%s %s</label>' % (label_for, rendered_cb, option_label)
         #   )
            sel = u''
            try:
                if option_value == force_unicode(value[0]) and self.select_mode != 3:
                    sel = u' selected '
                elif option_value in force_unicode(value) and self.select_mode == 3:
                    sel = u' selected '
            except IndexError:
                pass
            output.append(u'<option value="%s" name="%s" id="id_%s_%s" %s> '
                          u'%s</option>' % (option_value, name, name, option_value, sel, option_label))

        output.append(u'</select>')
        output.append(u'<script type="text/javascript">')
        js_data_var = 'fancytree_data_%s' % (attrs['id'].replace('-', '_'))
        if has_id:
            output.append(u'var %s = %s;' % (
                js_data_var,
                json.dumps(get_tree(self.queryset, str_values, self.hide_folder_checkbox))
            ))
            output.append(
                """
                $(".fancytree_checkboxes").hide();
                $(function() {
                    $("#f%(id)s").fancytree({

                        checkbox: true,
                        clickFolderMode: 2,
                        activeVisible: true,
                        selectMode: %(select_mode)d,
                        source: %(js_var)s,
                        debugLevel: %(debug)d,
                        beforeSelect: function(event, data){
                         // A node is about to be selected: prevent this, to limit node selections:
                             if( $('#%(id)s option:selected').length == 5 &! data.node.isSelected() ){
                             alert('You can only choose 5!');
                             return false;
                              }
                         },
                        select: function(event, data) {
                        //    $('#%(id)s').prop('selectedIndex',0);
                            $("#%(id)s option:selected").prop("selected", false);
                            var selNodes = data.tree.getSelectedNodes();
                            var selKeys = $.map(selNodes, function(node){
                                   $('#%(id)s_' + (node.key)).prop('selected', true);
                                   $( "#%(id)s" ).change();
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
                    'js_var': js_data_var,
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
