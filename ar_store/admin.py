from django.contrib import admin
from .models import Category,ProductRegistration,Contact



admin.site.register(Category)
admin.site.register(Contact)





@admin.register(ProductRegistration)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_added',
        'quantity'
        )  # Add 'created_at' here to show in the list view.
    readonly_fields = ('date_added',)  # Mark 'created_at' as readonly in the admin form.