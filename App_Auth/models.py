from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.utils import timezone
# Create your models here.

class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        if not email:
            raise ValueError('user must have an email address')
        if not phone:
            raise ValueError('user must have username')
        
        user = self.model(
            email = self.normalize_email(email),
            phone = phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone, password):
        user = self.create_user(
            email = self.normalize_email(email),
            phone = phone,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)

class User(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, blank=True, null=True, default='')
    last_name = models.CharField(max_length=50, blank=True, null=True, default='')
    email = LowercaseEmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=100, blank=True, null=True, default="", unique=True)
    gender = models.BooleanField(default=True)
    team = models.CharField(max_length=50, blank=True, null=True, default='')
    auth_code = models.CharField(max_length=50, blank=True, null=True, default='')
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50, blank=True, null=True, default='')
    sector = models.CharField(max_length=50, blank=True, null=True, default='')
    profile_image = models.ImageField(upload_to='profile_images', default='', blank=True, null=True)
    
    # required
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)
    modify_date = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class Team(models.Model):
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="teams")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Sector(models.Model):
    sector_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="sectors")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Role(models.Model):
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="roles")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class AuthCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auth_code = models.CharField(max_length=50, blank=True, null=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.auth_code






