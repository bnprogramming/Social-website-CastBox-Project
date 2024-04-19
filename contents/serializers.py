from rest_framework import serializers

from contents.models import Category, Tag, Channel, Episode


# region : Topics Serializers(Category,Tag)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = Category.get_list_fields()
        read_only_fields = ['url', 'slug', 'type', 'create_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = Tag.get_list_fields()
        read_only_fields = ['url', 'slug', 'type', 'create_at']


# endregion : Topics  Serializers(Category,Tag)


# region : Content Providers Serializers(Channel)
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = Channel.get_list_fields()
        read_only_fields = ['author', 'url', 'slug', 'followers_count', 'likes_count', 'comments_count']

    author = serializers.ReadOnlyField(source='author.get_full_name')
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['tag'] = TagSerializer(instance.tag).data
        return representation

# endregion : Content Providers Serializers(Channel)


# region : Final Content Serializers(Episode,Show)

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = Episode.get_list_fields()
        read_only_fields = ['url', 'slug', 'view_count', 'likes_count', 'comments_count']

    provider = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all())

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['provider'] = ChannelSerializer(instance.provider).data
        return representation

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        providers = Channel.objects.filter(author_id=user).all()
        self.fields['provider'].queryset = providers
        super().__init__(*args, **kwargs)


# endregion : Final Content Serializers(Episode,Show)
