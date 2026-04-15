from django.contrib import admin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name',)
    prepopulated_fields = {'cat_slug':('cat_name',)}
admin.site.register(Category, CategoryAdmin)
