from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


class UserAccountManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError("Users must have an email.")
    
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)

    user.set_password(password)
    user.save()

    return user
  
  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True')
    
    user = self.create_user(email, password, **extra_fields)

    return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(max_length=255, unique=True)
  phone_number = PhoneNumberField()
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  addresses = models.ManyToManyField('Address', related_name='users')

  objects = UserAccountManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

  def get_full_name(self):
    return f"{self.first_name} {self.last_name}"
  
  def get_short_name(self):
    return f"{self.first_name}"
  
  def __str__(self):
    return self.email
  

class Country(models.Model):
  country_name = models.CharField(max_length=55)


class Address(models.Model):
  unit_number = models.IntegerField()
  street_number = models.IntegerField()
  address_line1 = models.CharField(max_length=35)
  address_line2 = models.CharField(max_length=35, blank=True)
  city = models.CharField(max_length=25)
  region = models.CharField(max_length=25)
  postal_code = models.IntegerField()
  country = models.ForeignKey(Country, on_delete=models.PROTECT)

  def __str__(self):
    return f"{self.country}, {self.region}, {self.city}"