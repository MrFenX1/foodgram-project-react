from django.contrib import admin

from .models import Subscribe, CustomUsers


admin.site.register(CustomUsers)
admin.site.register(Subscribe)
