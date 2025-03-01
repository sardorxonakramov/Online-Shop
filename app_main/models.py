from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="catigory/",
        default="https://i.ytimg.com/vi/2QvOxa_7wEw/maxresdefault.jpg",
    )

    def __str__(self):
        return self.name
    
class Products(models.Model):
    title = models.CharField(max_length=100)  # Mahsulot nomi (maksimal uzunligi 100)
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE)  # Mahsulot kategoriyasi (agar kategoriya o'chirilsa, mahsulotlar ham o'chadi)
    description = models.TextField(blank=True, null=True)  # Mahsulot tavsifi (ixtiyoriy, bo'sh bo'lishi mumkin)
    image = models.ImageField(upload_to="products_img/", default='products_img/default.jpg')  # Mahsulot rasmi (agar rasm mavjud bo'lmasa, default rasm)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)  # Mahsulotning eski narxi
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Chegirma foizi (max 5 raqam, 2 raqamli o'nlik)
    new_price = models.DecimalField(editable=False, max_digits=10, decimal_places=2)  # Yangi narx (faqat avtomatik hisoblanadi)

    def save(self, *args, **kwargs):
        # Yangi narxni hisoblash: eski narxdan chegirma foizini chiqarish
        self.new_price = self.old_price - (self.old_price * (self.discount_percentage / 100))
        super().save(*args, **kwargs)  # Modelni saqlash

    def __str__(self):
        return self.title  # Mahsulot nomini qaytaradi



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Foydalanuvchiga bog'langan savat (bir foydalanuvchiga bitta savat)
    created_at = models.DateTimeField(auto_now_add=True)  # Savat yaratish vaqti (avtomatik tarzda saqlanadi)

    def __str__(self):
        return f"Cart for {self.user.first_name}"  # Savat nomi: Foydalanuvchi nomi

    def total_price(self):
        # Savatdagi barcha mahsulotlarning jami narxini hisoblash
        return sum(item.total_price for item in self.cartitem_set.all())

class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)  # Mahsulotga bog'langan savatdagi mahsulot
    quantity = models.PositiveIntegerField(default=1)  # Mahsulotning miqdori (default 1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foydalanuvchiga bog'langan
    added_at = models.DateTimeField(auto_now_add=True)  # Mahsulotni savatga qo'shish vaqti
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_cart_item')
        ]
    def __str__(self):
        return f"{self.product.title} x {self.quantity}"  

    @property
    def total_price(self):
        return self.product.new_price * self.quantity 
