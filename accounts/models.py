# -*- coding: utf-8 -*-
import re
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import BaseUserManager
from model_utils import Choices


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        app_label = "accounts"
        db_table = "user"

    username = models.CharField(_('username'), max_length=75, unique=True, required=True,
		help_text=_('Required. 30 characters or fewer. Letters, numbers and '
					'@/./+/-/_ characters'),
		validators=[
			validators.RegexValidator(re.compile('^[\w.@+-]+$'),
			_('Enter a valid username.'), 'invalid')
		])

	is_active = models.BooleanField(_('active'), default=False )
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['username']

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	def __unicode__(self):
		return self.email


class UserManager(BaseUserManager):
    use_in_migrations = True

    # envoked with regular users
    def create_user(self, username, password, **extras):
        if not username:
            raise ValueError('username is required')

        user = self.model(
            username=username,
            **extras
        )

        # set_password will take take of the hashing
        user.set_password(password)
        user.save()

        return user

    # envoked with superuser
    def create_superuser(self, username, password, **extras):
        if not username:
            raise ValueError('username is required')

        user = self.model(
            username=username,
            **extras
        )

        user.set_password(password)
        user.is_superuser = True
        user.save()

        return user
