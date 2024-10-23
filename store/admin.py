from django.contrib import admin
from .models import Category,Customer,  Proudct, Order, Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Proudct)
admin.site.register(Order)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile
 
 #extands User 
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name', 'email']
    inlines =[ProfileInline]
    
# unregister cause django
admin.site.unregister(User)

# register back
admin.site.register(User, UserAdmin)