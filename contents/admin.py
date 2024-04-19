from django.contrib import admin

from contents.models import Category, Tag, Channel, Episode
from utils.admin_class import ClassBaseAdmin

display = ['id', 'name', 'url', 'slug', 'image', 'create_at', 'is_active', 'is_deleted']
display_links = ['id', 'name', 'url', ]
filters = ['create_at', 'is_active', ]
search_words = ['id', 'name', 'url', 'slug', 'description', ]


# region : Topics model admin (Category, Tag)

@admin.register(Category)
class CategoryAdmin(ClassBaseAdmin, admin.ModelAdmin):
    list_display = display + ['country', ]
    list_display_links = display_links
    list_filter = filters + ['country', ]
    search_fields = search_words


@admin.register(Tag)
class TagAdmin(ClassBaseAdmin, admin.ModelAdmin):
    list_display = display + ['country', ]
    list_filter = filters + ['country', ]
    list_display_links = display_links
    search_fields = search_words


# endregion : Topics model admin (Category, Tag)

# region : Content providers model admin (Networks, Channels)

@admin.register(Channel)
class ChannelAdmin(ClassBaseAdmin, admin.ModelAdmin):
    list_display = display + ['author', 'tag', 'category', 'followers_count', 'likes_count',
                              'comments_count', ]
    list_display_links = display_links
    list_filter = filters + ['author', 'tag', 'category']
    search_fields = search_words


# endregion : Content providers model admin (Networks, Channels)

# region : Final Contents  model admin (Episodes, Shows)
@admin.register(Episode)
class EpisodeAdmin(ClassBaseAdmin, admin.ModelAdmin):
    list_display = display + ['provider', 'music', 'duration', 'view_count', 'likes_count', 'comments_count', ]
    list_display_links = display_links
    list_filter = filters + ['provider', ]
    search_fields = search_words

# endregion : Final Contents  model admin (Episodes, Shows)
