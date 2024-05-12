from django.contrib import admin
from .models import Owner, Breakfast, Lunch, Dinner, Cart, Order, Contact

# Register your models here.
admin.site.register(Owner)
admin.site.register(Breakfast)
admin.site.register(Lunch)
admin.site.register(Dinner)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Contact)
