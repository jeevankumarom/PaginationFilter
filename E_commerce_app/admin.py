from django.contrib import admin
from .models import categories,category_list
# Register your models here.

admin.site.register(category_list)
admin.site.register(categories)