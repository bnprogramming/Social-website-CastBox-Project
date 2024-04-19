from abc import abstractmethod
from django.db import models
from django.utils.text import slugify

from contents.models import Episode, Channel
from users.models import User


# Create your models here.

class BaseModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='create_at')
    is_active = models.BooleanField(default=True, verbose_name='is_active')
    is_deleted = models.BooleanField(default=False, verbose_name='is_deleted')

    class Meta:
        abstract = True

    def __str__(self):
        pass

    @classmethod
    def get_all_objects(cls):
        return cls.objects.all()

    @classmethod
    def get_list_fields(cls):
        return ['id', 'url', 'slug', 'image', 'create_at', 'is_active', 'is_deleted']


# region : user base
class Playlist(BaseModel):
    name = models.CharField(max_length=100, verbose_name='name')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    episodes = models.ManyToManyField(Episode, verbose_name='episodes', related_name='episodes_playlist', null=True,
                                      blank=True)

    url = models.URLField(verbose_name="URL", null=True, blank=True)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=250, unique=True,
                            verbose_name='slug')

    image = models.ImageField(upload_to='images/playlists', verbose_name="image", null=True, blank=True)
    type = models.CharField(max_length=20, verbose_name="type", null=True, blank=True)

    class Meta:
        verbose_name = 'playlist'
        verbose_name_plural = 'playlists'

    def __str__(self):
        return self.name

    @classmethod
    def get_list_fields(cls):
        main_list = super().get_list_fields()
        return main_list + ['user', 'name', 'episodes']

    def save(self, *args, **kwargs):
        self.type = 'playlist'
        self.name = self.name.title()
        self.slug = slugify(self.name)
        self.url = (f'http://localhost:8000/playlist/' + self.slug)
        super().save(*args, **kwargs)


class UserItem(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    def __str__(self):
        return f'{self.item.slug}'


class Like(UserItem):
    item = models.ForeignKey(Episode, on_delete=models.CASCADE, verbose_name='Episode_liked', null=True, blank=True)

    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'likes'


class Follow(UserItem):
    item = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name='Channel_Followed', null=True, blank=True)

    class Meta:
        verbose_name = 'follow'
        verbose_name_plural = 'follows'


class Comment(UserItem):
    item = models.ForeignKey(Episode, on_delete=models.CASCADE, verbose_name='Episode_Comment', null=True, blank=True)

    text = models.TextField(verbose_name='text')
    parent = models.ForeignKey('self', verbose_name='Answer', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

# endregion


# region : client base
class View(BaseModel):
    client = models.CharField(max_length=500, verbose_name='client', null=True, blank=True, )
    item = models.ForeignKey(Episode, on_delete=models.CASCADE, verbose_name='episode_viewed')

    class Meta:
        verbose_name = 'view'
        verbose_name_plural = 'views'

    def __str__(self):
        return f'user:({self.client}) - Item:({self.item.slug})'
# endregion
