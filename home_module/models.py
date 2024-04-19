from django.db import models
from django.utils.text import slugify


# Home models:

class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="country", db_index=True, unique=True)
    nickname = models.CharField(max_length=10, verbose_name="nickname", db_index=True, unique=True, )
    slug = models.SlugField(max_length=250, default="", null=False, db_index=True, blank=True, unique=True,
                            verbose_name='slug')
    query = models.CharField(max_length=500, default="", null=False, blank=True, verbose_name="query", unique=True)
    is_active = models.BooleanField(default=True, verbose_name="is_active")

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name

    @classmethod
    def get_list_fields(cls):
        return ['id', 'name', 'nickname', 'query', 'is_active']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.query = '?country=' + self.nickname.lower()
        self.name = self.name.lower().strip().replace(' ', '-')
        super().save(*args, **kwargs)
