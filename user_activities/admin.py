from django.contrib import admin

from user_activities.models import Playlist, Like, View, Follow, Comment
from utils.admin_class import ClassBaseAdmin

display_items = ['id', 'user', 'create_at', 'is_active', 'is_deleted']
filter_items = ['create_at', 'is_active', 'is_deleted']


# Register your models here.

@admin.register(Playlist)
class PlaylistAdmin(ClassBaseAdmin, admin.ModelAdmin):
    list_display = display_items + ['name', 'url', 'slug']
    list_display_links = ['name', ]
    list_filter = ['user'] + filter_items
    search_fields = ['name', 'slug']


class BasicAdmin(ClassBaseAdmin, admin.ModelAdmin):
    list_display = display_items + ['item', ]

    list_filter = ['user'] + filter_items
    search_fields = ['user', ]


@admin.register(Like)
class LikeAdmin(BasicAdmin):
    pass

@admin.register(Follow)
class FollowAdmin(BasicAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(BasicAdmin):
    list_display = BasicAdmin.list_display + ['item', 'text', 'parent', ]


@admin.register(View)
class ViewAdmin(ClassBaseAdmin, admin.ModelAdmin):
    list_display = ['id', 'client'] + filter_items
    list_display_links = ['client', ]
    list_filter = ['client', ] + filter_items
    search_fields = ['client', ]
