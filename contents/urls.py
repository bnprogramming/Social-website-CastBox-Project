from django.urls import path

from contents.views import CategoryListView, TagListView, EpisodeListView, EpisodeDetailView, ChannelListView, TopicItemsListView

urlpatterns = [

    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/<category>', EpisodeListView.as_view(), name='episode_categories_list'),

    path('tag/', TagListView.as_view(), name='tag_list'),
    path('tag/<tag>', EpisodeListView.as_view(), name='episode_tags_list'),


    path('channel/', ChannelListView.as_view(), name='channel-list'),
    path('channel/<channel>', EpisodeListView.as_view(), name='episode_channels_list'),

    path('episode-list/', EpisodeListView.as_view(), name='episode_list'),
    path('episode/<slug>', EpisodeDetailView.as_view(), name='episode_detail'),


    path('related-items/<topic>/<slug>', TopicItemsListView.as_view(), name='related_items_list')

]
