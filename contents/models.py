from django.db import models
from django.utils.text import slugify

from home_module.models import Country
from users.models import User

content_address = 'http://localhost:8000/content/'


# Content models:
class BaseModel(models.Model):
    type = models.CharField(max_length=20, verbose_name="type", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="name", default="")
    url = models.URLField(verbose_name="URL", null=True, blank=True)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=250, unique=True,
                            verbose_name='slug')
    description = models.TextField(verbose_name="description", default="Nothing", null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="create_at", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    is_deleted = models.BooleanField(default=False, verbose_name="is_deleted")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @classmethod
    def get_actives(cls):
        return cls.objects.filter(is_active=True, is_deleted=False)

    @classmethod
    def get_all_objects(cls):
        return cls.objects.all()

    @classmethod
    def get_list_fields(cls):
        return ['id', 'name', 'url', 'slug', 'image', 'description', 'create_at', 'is_active', 'is_deleted']

    @classmethod
    def get_new_items(cls):
        return cls.get_actives().order_by('-create_at')[:18]


# region : Topics models (Category, Tag)
class Topics(BaseModel):
    country = models.ForeignKey(Country, verbose_name="country", on_delete=models.CASCADE, null=True, default=None)

    @classmethod
    def get_list_fields(cls):
        main_list = super().get_list_fields()
        return main_list + ['image', 'country']


class Category(Topics):
    image = models.ImageField(upload_to='images/categories', verbose_name="image", null=True, blank=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        self.type = 'category'
        self.name = self.name.title()
        self.slug = slugify(self.name)
        self.url = (content_address + 'category/' + self.slug)
        super().save(*args, **kwargs)


class Tag(Topics):
    image = models.ImageField(upload_to='images/tags', verbose_name="image", null=True, blank=True)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def save(self, *args, **kwargs):
        self.type = 'tag'
        self.name = self.name.title()
        self.slug = slugify(self.name)
        self.url = (content_address + 'tag/' + self.slug)
        super().save(*args, **kwargs)


# endregion : Topics models (Category, Tag)


# region : Content providers models (Channels)
class Channel(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="author")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="tag", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category', null=True, blank=True)

    image = models.ImageField(upload_to='images/channels', verbose_name="image")

    followers_count = models.IntegerField(verbose_name="followers", default=0)
    likes_count = models.IntegerField(verbose_name="like_count", default=0)
    comments_count = models.IntegerField(verbose_name="comments_count", default=0)

    class Meta:
        verbose_name = "channel"
        verbose_name_plural = "channels"

    def save(self, *args, **kwargs):
        self.type = 'channel'
        self.slug = slugify(self.name)
        self.url = (content_address + 'channel/' + self.slug)
        super().save(*args, **kwargs)

    @classmethod
    def get_list_fields(cls):
        main_list = super().get_list_fields()
        return main_list + ['author', 'tag', 'category', 'followers_count', 'comments_count', 'image', ]

    @classmethod
    def get_popular_items(cls):
        return cls.get_actives().order_by('-likes_count')[:8]

    @classmethod
    def get_most_followed_items(cls):
        return cls.get_actives().order_by('-followers_count')[:8]


# endregion : Content providers models (Channels)


# region : Final Contents  models (Episodes)

class Episode(BaseModel):
    provider = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name="channel")
    mentions = models.ManyToManyField(User, related_name='mention_provider', verbose_name="mention_provider",
                                      default=None, null=True, blank=True)

    image = models.ImageField(upload_to='images/episodes/', verbose_name="image")
    music = models.FileField(upload_to='musics/episodes/', verbose_name="music")
    duration = models.DurationField(verbose_name="duration", default=0)

    view_count = models.IntegerField(verbose_name="views_count", default=0)
    likes_count = models.IntegerField(verbose_name="likes_count", default=0)
    comments_count = models.IntegerField(verbose_name="comments_count", default=0)

    @classmethod
    def get_list_fields(cls):
        main_list = super().get_list_fields()
        return main_list + ['provider', 'mentions', 'image', 'music', 'duration', 'view_count', 'likes_count',
                            'comments_count', ]

    @classmethod
    def get_most_liked_items(cls):
        return cls.get_actives().order_by('-likes_count')[:8]

    @classmethod
    def get_most_visited_items(cls):
        return cls.get_actives().order_by('-view_count')[:8]

    def save(self, *args, **kwargs):
        self.type = 'episode'
        self.slug = slugify(self.name)
        self.url = (content_address + 'episode/' + self.slug)
        super().save(*args, **kwargs)

# endregion : Final Contents  models (Episodes)
