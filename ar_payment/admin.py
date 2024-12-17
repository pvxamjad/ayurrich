from django.contrib import admin
from .models import ShippingAddress,OrderProducts,OrderSummary

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(OrderProducts)

@admin.register(OrderSummary)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'total_amount',
        'is_shipped'
        )  # Add 'created_at' here to show in the list view.
    readonly_fields = ('orderd_date','shipped_date',)  # Mark 'created_at' as readonly in the admin form.