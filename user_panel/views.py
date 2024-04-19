from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from contents.models import Episode, Channel
from contents.serializers import ChannelSerializer, EpisodeSerializer

from user_activities.models import Playlist, Like, Follow
from user_activities.serializer import PlaylistSerializer


# region : main user panel view(menu items)
@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


@login_required
def user_panel_menu_component(request):
    user = request.user
    context = {'user': user}
    return render(request, 'user_panel_module/components/user_panel_menu_component.html', context)


# endregion : main user panel view(menu items)


# region : user_panel items base view
@method_decorator(login_required, name='dispatch')
class UserBaseViewSetApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pass

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# endregion

# region : User Channels
class UserChannel(UserBaseViewSetApiView):
    serializer_class = ChannelSerializer

    def get_queryset(self):
        user = self.request.user
        return Channel.objects.filter(author=user)


# endregion : User Channels

# region : User Episodes

class UserEpisode(UserBaseViewSetApiView):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        user = self.request.user
        return Episode.objects.filter(provider__author=user)

    def perform_create(self, serializer):
        serializer.save()


# endregion : User Episodes

# region : User Playlist view
class UserAddPlalistViewSetApiView(UserBaseViewSetApiView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserPlaylistListView(mixins.ListModelMixin, ListView):
    context_object_name = 'objects'
    template_name = 'content_page.html'

    model = Playlist

    def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Playlist'
        context['icon'] = 'play'
        return context


class PlaylistItemsListView(mixins.ListModelMixin, ListView):
    context_object_name = 'objects'
    template_name = 'content_page.html'
    playlist_slug = ""

    def get_queryset(self):
        playlist_slug = self.kwargs['slug']
        playlist = Playlist.objects.get(slug=playlist_slug)
        self.playlist_slug = playlist_slug
        all_related_episodes = playlist.episodes.all()
        return list(all_related_episodes)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Playlist Items'
        context['icon'] = 'play'
        context['playlist'] = self.playlist_slug
        return context


class PlaylistDelete(View):
    def get(self, request, *args, **kwargs):
        playlist_id = self.kwargs.get('id')
        playlist = Playlist.objects.get(pk=playlist_id)
        playlist.delete()
        return redirect(reverse('user_playlists_view'))


class PlaylistItemDelete(View):
    def get(self, request, *args, **kwargs):
        playlist_slug = self.kwargs.get('playlist')
        item_id = self.kwargs.get('id')
        item_type = self.kwargs.get('type')

        playlist = Playlist.objects.get(slug=playlist_slug)
        if item_type == 'episode':
            item = Episode.objects.get(pk=item_id)
            playlist.episodes.remove(item)

        return redirect(reverse('user_playlists_view'))


# endregion : User Playlist view

# region : User Favorites view
@method_decorator(login_required, name='dispatch')
class UserFavoritesList(mixins.ListModelMixin, ListView):
    context_object_name = 'objects'
    template_name = 'content_page.html'
    model = Like

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = Like.objects.filter(user=self.request.user)
        context['title'] = 'Favorites'
        context['icon'] = 'heart'
        return context


# endregion : User Playlist view

# region : User Followings view
@method_decorator(login_required, name='dispatch')
class UserFollowingChannelsList(mixins.ListModelMixin, ListView):
    context_object_name = 'objects'
    template_name = 'content_page.html'
    model = Follow

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = Follow.objects.filter(user=self.request.user)
        context['title'] = 'Followings'
        context['icon'] = 'users'
        return context
# endregion : User Followings view
