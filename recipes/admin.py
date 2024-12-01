from django.contrib import admin
from .models import Recipe, Category, Comment, Like, Following

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Following)
