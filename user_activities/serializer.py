from rest_framework import serializers

from contents.serializers import EpisodeSerializer
from user_activities.models import Playlist


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = Playlist.get_list_fields()
        read_only_fields = ['user', 'slug', 'url', 'episodes']

    user = serializers.ReadOnlyField(source='user.get_full_name')
