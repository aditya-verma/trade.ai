from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

from trade_ai.accounts.managers import UserManager
from trade_ai.base.models import TradeAIBaseModel
from trade_ai.base.validators import user_age_validator


class USER_TYPES(object):
    """Object class to represent type of User(s) on Marketplace.
    """
    EMPLOYEE_L1 = 1
    CUSTOMER = 2
    PANDIT = 3


class User(AbstractBaseUser, PermissionsMixin, TradeAIBaseModel):
    """Django model class to represent User table.
    """
    USER_TYPE_CHOICES = (
        (None, 'Please select a valid User type'),
        (USER_TYPES.EMPLOYEE_L1, 'Level 1 Employee'),
        (USER_TYPES.CUSTOMER, 'Customer'),
    )
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES,
                                    default=USER_TYPES.CUSTOMER)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, blank=True, null=False)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        validators=[user_age_validator]
    )
    GENDER_TYPE_CHOICES = (
        (None, 'Not Specified'),
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Others'),
    )
    gender = models.IntegerField(choices=GENDER_TYPE_CHOICES,
                                 blank=True,
                                 null=True,
                                 default=None)
    referral_code = models.CharField(
        max_length=32,
        blank=True,
        null=False,
        help_text='Referral code of User, auto-generated on KYC verification.'
    )
    jwt_token_secret = models.CharField(max_length=12, default=get_random_string)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # To track Activation and De-activation of User's account, so that system
    # can wipe all the data after n days of de-activation of account.
    activated_at = models.DateTimeField(blank=True, null=True)
    deactivated_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = EMAIL_FIELD = 'email'
    username = None

    REQUIRED_FIELDS = ('mobile_no', 'first_name', 'middle_name', 'last_name', )

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def refresh_jwt_token(self):
        self.jwt_token_secret = get_random_string()

        self.save(update_fields=['jwt_token_secret'])

        return True

    def fetch_jwt_token(self):
        payload = {
            'email': self.email,
            'exp': int(
                (
                    datetime.now() + timedelta(
                        days=settings.JWT_TOKEN_VALIDITY_DAYS
                    )
                ).timestamp()
            )
        }

        jwt_token_django_secret = f'{self.jwt_token_secret}{settings.SECRET_KEY}'

        return jwt.encode(payload, jwt_token_django_secret, algorithm='HS256')
