from django.contrib import admin
from .models import *

# Đăng ký các mô hình
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Restaurant)
admin.site.register(Shipper)
admin.site.register(Menu)
admin.site.register(History)
admin.site.register(ReviewMenu)
admin.site.register(Review)
admin.site.register(Message)
admin.site.register(Voucher)
admin.site.register(Role)
admin.site.register(FoodType)
admin.site.register(FavoriteRestaurant)
admin.site.register(FavoriteMenu)
admin.site.register(Cart)

