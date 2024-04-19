from itertools import chain

from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from rest_framework import mixins

from contents.models import Category, Tag, Episode, Channel
from user_activities.models import View, Like, Comment
from utils.convertors import group_list


# Create your views here.

class BaseListView(mixins.ListModelMixin, ListView):
    context_object_name = 'objects'
    template_name = 'content_page.html'


class CategoryListView(BaseListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categories'
        context['icon'] = 'archive'
        return context


class TagListView(BaseListView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tags'
        context['icon'] = 'bandcamp'

        return context


class TopicItemsListView(TemplateView):
    template_name = 'object_module/object_list.html'

    def get_context_data(self, **kwargs):
        topic = self.kwargs['topic']
        context = super(TopicItemsListView, self).get_context_data(**kwargs)
        if topic == "category":
            all_related_channel = Channel.objects.filter(category__slug=self.kwargs['slug']).all()
        elif topic == "tag":
            all_related_channel = Channel.objects.filter(tag__slug=self.kwargs['slug']).all()
        else:
            all_related_channel = None
        context['related_providers'] = list(all_related_channel)

        return context


class EpisodeListView(ListView):
    template_name = 'episode_module/episode_list.html'
    model = Episode
    context_object_name = 'episodes'
    ordering = ['-likes_count']
    paginate_by = 8

    def get_queryset(self):
        query = super(EpisodeListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        channel_name = self.kwargs.get('channel')
        tag_name = self.kwargs.get('tag')

        if category_name is not None:
            query = query.filter(provider__category__slug__iexact=category_name)
        elif channel_name is not None:
            query = query.filter(provider__slug__iexact=channel_name)
        elif tag_name is not None:
            query = query.filter(provider__tag__slug__iexact=tag_name)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episodes'] = group_list(list(context['episodes']), 4)
        return context


class EpisodeDetailView(DetailView):
    template_name = 'episode_module/episode_detail.html'
    model = Episode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        episode = Episode.objects.get(slug=self.kwargs.get('slug'))
        related_episode = list(
            Episode.objects.filter(is_active=True, provider_id=episode.provider_id).exclude(pk=episode.id).all()[:4])
        context['related_episodes_by_channel'] = related_episode
        context['episode'] = episode
        context['mentions'] = list(episode.mentions.filter().values_list('username', flat=True))
        context['comments'] = Comment.objects.filter(item_id=episode.id, parent_id=None).order_by('-create_at').prefetch_related(
            'comment_set')
        context['comments_count'] = Comment.objects.filter(item_id=episode.id).count()

        # region :make a view log for episode
        client_specifications = self.request.META.get('HTTP_USER_AGENT')
        view_record, state = View.objects.get_or_create(client=client_specifications, item=episode)
        if state:
            view_record.item = episode
            view_record.is_active = True
            view_record.is_deleted = False
            view_record.save()
        # endregion

        # update views and likes
        episode.comments_count = context['comments_count']
        episode.likes_count = Like.objects.filter(item=episode).count()
        episode.view_count = View.objects.filter(item=episode).count()
        episode.save()
        return context


class ChannelListView(ListView):
    template_name = 'channel_module/channel_list.html'
    model = Channel
    context_object_name = 'channels'
    ordering = ['-followers_count']  # sort channels by number of followers
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authentication'] = self.request.user.is_authenticated
        context['channels'] = group_list(list(context['channels']), 4)

        return context


def content_component(request):
    return render(request, 'components/content_component.html', {})


def sidebar_categories_component(request):
    episode_categories = list(Category.objects.filter(is_active=True).all())[-5:]
    context = {
        'episode_categories': episode_categories,
    }
    return render(request, 'episode_module/components/sidebar_categories_component.html', context)


def sidebar_channels_component(request):
    episode_channels = list(Channel.objects.filter(is_active=True).all())[-5:]
    context = {
        'episode_channels': episode_channels,
    }
    return render(request, 'episode_module/components/sidebar_channels_component.html', context)


def sidebar_tags_component(request):
    episode_tags = list(Tag.objects.filter(is_active=True).all())[-5:]
    context = {
        'episode_tags': episode_tags,
    }
    return render(request, 'episode_module/components/sidebar_tags_component.html', context)
