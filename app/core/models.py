import uuid
import os
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)

from django.conf import settings


def recipe_image_file_path(instance, filename):
    """
    Generate file path for new recipe image
    """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):

    # password = None in case you need to create a user that is not active
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new User
        """
        if not email:
            raise ValueError('Users must have email address!')
        # normalize_email func makes email lowercase in case user provides Uppercase
        user = self.model(email=self.normalize_email(email), **extra_fields)
        #password has to be encrypted so we need to use set_password function
        user.set_password(password)
        # saving user with options "using=self._db" means that
        # multiple databases can be used in case we use more than 1 database in our project
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a new super user
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email insted of username
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # to determine if user is active or not, in case we want to deactivate user if we need
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    #by default it is user name but we want to change it to email
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """
    Tag to be used for a recipe
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ingredient to be usen recipe
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Recipe object
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
     )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
