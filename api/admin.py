from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'idRoles', 'is_approved', 'phoneNumber', 'email', 'is_active')
    list_filter = ('idRoles', 'is_approved', 'is_active')

    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)

    approve_users.short_description = "Approuver les utilisateurs sélectionnés"


# admin.py

from django.contrib import admin
from .models import Image, ModelsTenue

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'categorie', 'image_file')
    search_fields = ['name', 'categorie']

@admin.register(ModelsTenue)
class ModelsTenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'categorie', 'temps_execution', 'prix', 'image')
    search_fields = ['name', 'categorie']


admin.site.register(CustomUser, CustomUserAdmin)
