from django.db.models import EmailField, CharField, BooleanField, DateTimeField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, name=None, full_name=None, is_active=None, is_staff=None, is_admin=None):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('Пользователь должен иметь email')
        if not password:
            raise ValueError('Пользователь должен ввести пароль')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password, is_staff=True, is_admin=True)
        return user

    def create_staffuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password, is_staff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True, max_length=255)
    name = CharField(max_length=255, blank=True, null=True)
    full_name = CharField(max_length=255, blank=True, null=True)
    staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    admin = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        if self.name:
            return self.name
        else:
            return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        else:
            return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        print(self.password)
        super().save(*args, **kwargs)
