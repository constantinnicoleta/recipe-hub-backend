from django.contrib import admin
from .models import Recipe, Category, Following

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Following)
