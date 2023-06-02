from django.contrib import admin

from .models import Subscribe, CustomUsers


@admin.register(CustomUsers)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')
    empty_value_display = '<пусто>'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_author')
    search_fields = ('user', 'user_author')
    list_filter = ('user', 'user_author')
    empty_value_display = '<пусто>'