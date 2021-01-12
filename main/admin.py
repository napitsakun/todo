from django.contrib import admin
from .models import *

# Register your models here.


class RegisteredUserAdmin(admin.ModelAdmin):
	list_display = ('user', 'date_of_birth', )
	search_fields = ('first_name', 'last_name', 'user__username')
	list_filter = ('date_of_birth', )


class ToDoTaskAdmin(admin.ModelAdmin):
	list_display = ('task', 'created_by', 'is_active', )
	search_fields = ('task', 'created_by', )
	list_filter = ('created_by', 'created_at', 'updated_at', )
	readonly_fields = ('created_by', 'created_at', 'updated_at', )


admin.site.register(ToDoTask, ToDoTaskAdmin)
admin.site.register(RegisteredUser, RegisteredUserAdmin)
