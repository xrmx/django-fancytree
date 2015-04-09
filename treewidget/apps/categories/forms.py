from django import forms
from apps.categories.models import Category, Selection
from fancytree.widgets import FancyTreeWidget

categories = Category.objects.all()

class SelectionForm(forms.ModelForm):
    class Meta:
        model = Selection
        widgets = {
            'categories': FancyTreeWidget(queryset=categories)
        }
