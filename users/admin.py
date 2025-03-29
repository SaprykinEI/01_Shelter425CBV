from django.contrib import admin
from users.models import User

# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'pk')
    list_filter = ('last_name',)