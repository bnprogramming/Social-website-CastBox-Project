from django.urls import path

from user_activities.views import PlayListToAddView, AddToPlaylistView, like_item, follow_channel, \
    unfollow_channel, unlike_item, send_comment, delete_comment
from user_panel.views import PlaylistItemsListView

urlpatterns = [
    path('playlist-related-items/<slug>', PlaylistItemsListView.as_view(), name='playlist_related_items_list'),
    path('playlists-to-add/<item_slug>/<type>', PlayListToAddView.as_view(), name='playlists_to_add'),
    path('playlists-to-add/<playlist_id>/<type>/<item_slug>', AddToPlaylistView.as_view(), name='add_to_playlist'),

    path('like-item/<item_type>/<item_id>', like_item, name='like_item'),
    path('unlike-item/<item_type>/<item_id>', unlike_item, name='unlike_item'),

    path('follow-item/<item_id>', follow_channel, name='follow_channel'),
    path('unfollow-item/<item_id>', unfollow_channel, name='unfollow_channel'),

    path('send-comment/', send_comment, name='send_comment'),
    path('delete-comment/', delete_comment, name='delete_comment'),
]