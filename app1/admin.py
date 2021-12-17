from django.contrib import admin
from app1.models import *

class UsersAdmin(admin.ModelAdmin):
    pass
admin.site.register(Users, UsersAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

class CategoriasAdmin(admin.ModelAdmin):
    pass
admin.site.register(Categorias, CategoriasAdmin)

class OrdersAdmin(admin.ModelAdmin):
    pass
admin.site.register(Orders, OrdersAdmin)


class Order_detailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order_details, Order_detailsAdmin)

