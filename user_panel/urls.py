from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user_panel.views import UserEpisode, UserChannel, UserPanelDashboardPage, UserPlaylistListView, \
    PlaylistItemsListView, PlaylistDelete, PlaylistItemDelete, UserFavoritesList, UserFollowingChannelsList, \
    UserAddPlalistViewSetApiView

episode_router = DefaultRouter()
channel_router = DefaultRouter()
add_playlist_router = DefaultRouter()


episode_router.register('', UserEpisode, basename='episodes_view')
channel_router.register('', UserChannel, basename='channels_view')
add_playlist_router.register('', UserAddPlalistViewSetApiView, basename='add_plalist_view')

urlpatterns = [
    path('', UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    path('user-episode/', include(episode_router.urls), name='user_episodes_view'),
    path('user-channel/', include(channel_router.urls), name='user_channels_view'),

    path('user-playlist/', UserPlaylistListView.as_view(), name='user_playlists_view'),
    path('add-playlist/', include(add_playlist_router.urls), name='add_playlist_view'),
    path('user-playlist/<slug>', PlaylistItemsListView.as_view(), name='user_playlist_items_view'),

    path('playlist-delete/<int:id>', PlaylistDelete.as_view(), name='playlist_delete'),
    path('playlist-item-delete/<playlist>/<id>/<type>', PlaylistItemDelete.as_view(), name='playlist_item_delete'),

    path('favorites/', UserFavoritesList.as_view(), name='favorites_list'),
    path('followings/', UserFollowingChannelsList.as_view(), name='followings_list'),

]