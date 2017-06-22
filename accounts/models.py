# -*- coding: utf-8 -*-
import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    # create_user and create_superuser call this handler
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Username is not set.')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('SUPERUSER: Failed [is_staff=True]')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SUPERUSER: Failed [is_superuser=True]')

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    email = None
    first_name = None
    last_name = None

    is_active = models.BooleanField(default=False, verbose_name='active')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()
