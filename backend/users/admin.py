from django.contrib import admin
from .models import Follower, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')


@admin.register(Follower)
class UserAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')

