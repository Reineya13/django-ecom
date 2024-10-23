from django.contrib import admin
from .models import ShippingAddress, OrderItem, Order

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0
    
    # extands order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields=['date_order']
    fields = ['user', 'full_name', 'email', 'shipping_address', 'amount_paid', 'date_order', 'shipped','date_shipped']
    inlines = [OrderItemInLine]
    
# unregister cause django
admin.site.unregister(Order)

# register back
admin.site.register(Order, OrderAdmin)
        


