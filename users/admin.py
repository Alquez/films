from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'is_banned')}),
        ('Premium', {'fields': ('is_premium', 'premium_expiration')}),  # Add the is_premium field here
        ('Movies', {'fields': ('active_movie', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = [
        'username', 'email', 'first_name',
        'last_name', 'is_staff', 'is_premium']  # Add is_premium to the list_display
    list_filter = ('is_premium', "is_staff", "is_superuser", "is_active", "groups")

    filter_horizontal = (
        "groups",
        "user_permissions",
        "active_movie",
    )
