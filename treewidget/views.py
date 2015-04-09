from django.shortcuts import render, get_object_or_404, redirect
from apps.categories.forms import SelectionForm
from apps.categories.models import Selection


def home(request):
    form = SelectionForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            selection = form.save()
            return redirect('selection', pk=selection.pk)
    selections = Selection.objects.all()
    return render(request, "home.html", {'form': form, 'selections': selections})

def selection(request, pk):
    selection = get_object_or_404(Selection, pk=pk)
    if request.method == "POST":
        form = SelectionForm(request.POST, instance=selection)
        if form.is_valid():
            selection = form.save()
            return redirect('selection', pk=selection.pk)
    else:
        form = SelectionForm(instance=selection)
    selections = Selection.objects.all()
    return render(request, "home.html", {'form': form, 'selections': selections})
