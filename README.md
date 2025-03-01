
# Onlineshops Advanced

Bu loyiha onlayn savdo qilish uchun kengaytirilgan versiya bo'lib, Ushbu loyihada Category va kategoriyaning productalri mavjuda va backend orqali paginatsiya ham qilingan

## Xususiyatlar:
- **Kategoriya tizimi**: Mahsulotlar turkumlarga ajratilgan.
- **Social OAuth2 Authentication**: Foydalanuvchilar Google, Facebook va boshqa xizmatlar orqali tizimga kirishi mumkin.
- **Foydalanuvchi profilingi**: Har bir foydalanuvchi o'z shaxsiy hisob sahifasiga ega.
- **CRUD funksiyalari**: Mahsulotlar qo'shish, tahrirlash, o'chirish va ko'rish imkoniyati mavjud.
- **To'lov tizimi**: Xarid amalga oshirilganda, SMTP orqali emailga to'lov haqida xabar yuboriladi. **Diqqat**: To'lov tizimi to'liq ishlamasligi mumkin.

## O'rnatish
1. Loyihani yuklab oling:
   ```bash
   git clone https://github.com/sardorxonakramov/Onlineshops-Advanced.git
   cd Onlineshops-Advanced
   ```
2. Virtual muhitni yarating va faollashtiring:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # MacOS/Linux
   .venv\Scripts\activate     # Windows
   ```
3. Kerakli kutubxonalarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```
4. `.env` faylini yarating va kerakli maxfiy kalit va tokenlarni qo'shing.
5. Ma'lumotlar bazasini yangilang:
   ```bash
   python manage.py migrate
   ```
6. Serverni ishga tushiring:
   ```bash
   python manage.py runserver
   ```

## Foydalanish
1. Saytga tashrif buyuring: `http://127.0.0.1:8000`
2. Social OAuth2 orqali tizimga kiring yoki ro'yxatdan o'ting.
3. Mahsulotlarni ko'rib chiqing va savatchaga qo'shing.
4. Xarid qilish tugmachasini bosganda, email orqali to'lov xabari yuboriladi.

## Hissa qo'shish
1. Fork qiling.
2. O'zingizning branch-ingizni yarating: `git checkout -b yangi-branch`
3. O'zgarishlarni commit qiling: `git commit -m "O'zgarish tavsifi"`
4. O'z branch-ingizni push qiling: `git push origin yangi-branch`
5. Pull request jo'nating.

## Muallif
- **Sardorxon Akramov** - [GitHub Profilim](https://github.com/sardorxonakramov)

## Litsenziya
Ushbu loyiha [MIT](LICENSE) litsenziyasi asosida tarqatiladi.

