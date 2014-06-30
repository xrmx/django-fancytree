from django.contrib import admin

from apps.categories.models import Category

class CategoryAdminOption(admin.ModelAdmin):
    list_display = ("get_repr", "get_tree")
    ordering = ("url",)
    search_fields = ('name', )


admin.site.register(Category, CategoryAdminOption)
