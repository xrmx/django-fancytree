Django Fancytree Widget
----------------------

django-fancytree provides a widget using the fancytree js library to
render a forms.ModelMultipleChoiceField as a tree with selectable and
collapsable nodes.

See included project 'treewidget' as an example. Widget is used in
ModelMultipleChoiceField and allows user to select multiple categories.


Requirements
------------

django, django-mptt, jquery, jquery-ui


Usage
-----

::

  from fancytree.widgets import FancyTreeWidget

  categories = Category.objects.all()

  class CategoryForm(forms.Form):
      categories = forms.ModelMultipleChoiceField(
         queryset=categories,
         widget=FancyTreeWidget(queryset=categories)
      )


In this example Category is a model registered with django-mptt.

Widget accepts **queryset** option, which expects pre-ordered queryset by
"tree_id" and "lft".

If you want to adjust tree data creation, you can define 'get_doc' method on
your model. Example:

::

  def get_doc(self, values):
    doc = {"title": name, "key": self.pk}
    if str(self.pk) in values:
        doc['select'] = True
        doc['expand'] = True
    return doc
