from django.contrib import admin
from .models import Category, Products

# Category uchun oddiy ro‘yxat
# @admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Admin panelda ko‘rsatish uchun maydonlar
    search_fields = ('name',)  # Qidiruv panelida ishlatiladigan maydonlar
    list_filter = ('name',)  # Filtrlash uchun maydon



# Products uchun murakkabroq ro‘yxat
# @admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'old_price', 'new_price')  # Asosiy ma’lumotlar
    search_fields = ('title', 'category__name')  # Qidiruv uchun mahsulot va kategoriyalar nomi
    list_filter = ('category',)  # Filtr: kategoriya bo‘yicha
    readonly_fields = ('new_price',)  # Agar `new_price` dinamik hisoblanadigan bo‘lsa, o‘qish rejimida bo‘lishi kerak
    fields = ('title', 'category', 'description', 'old_price', 'discount_percentage','image')  # Tartibni sozlash

admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)