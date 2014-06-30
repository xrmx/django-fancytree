from django.shortcuts import render
from apps.categories.forms import CategoryForm


def home(request, template_name="home.html"):
    form = CategoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print form.cleaned_data
        else:
            print form.errors
    return render(request, template_name, {'form': form})
