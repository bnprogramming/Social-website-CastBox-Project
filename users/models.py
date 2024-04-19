from django.db import models
from django.contrib.auth.models import AbstractUser


# Base USER model:
class User(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name='phone', default="", null=True, blank=True)
    avatar = models.ImageField(upload_to='images/user_avatar', verbose_name='picture', null=True, blank=True)
    description = models.TextField(verbose_name='description', default="Nothing", null=True, blank=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()
        else:
            return self.username

    @classmethod
    def get_list_fields(cls):
        return ['username', 'first_name', 'last_name', 'email', 'password', 'phone', 'avatar', 'description',
                'is_active', 'date_joined']
