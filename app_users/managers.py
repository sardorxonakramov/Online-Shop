from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError


class UserModelManagers(UserManager):
    def create_user(
        self,
        email: str,
        first_name: str = "",
        last_name: str = "",
        password: str = None,
    ):
        # Tekshirish
        if not email:
            raise ValidationError("Email maydoni majburiy.")


        # Normalize email
        email = self.normalize_email(email)

        # Foydalanuvchi mavjudligini tekshirish
        if self.model.objects.filter(email=email).exists():
            raise ValidationError("Ushbu email bilan foydalanuvchi allaqachon mavjud.")

        # Foydalanuvchi yaratish
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password:str=None):
        superuser = self.create_user(
            email=email, first_name=first_name, last_name=last_name, password=password
        )
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser
