from django import forms
from apps.categories.models import Category
from fancytree.widgets import FancyTreeWidget

categories = Category.objects.all()

class CategoryForm(forms.Form):
    name = forms.CharField()
    categories = forms.ModelMultipleChoiceField(
        queryset=categories,
        widget=FancyTreeWidget(queryset=categories)
    )
