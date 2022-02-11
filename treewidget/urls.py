from django.contrib import admin
from django.urls import path

from treewidget.views import home, selection

admin.autodiscover()

urlpatterns = [
    path("", home, name='home'),
    path("selection/<pk>", selection, name='selection'),
    path("admin/", admin.site.urls),
]