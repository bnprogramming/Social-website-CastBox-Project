from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from rest_framework import mixins

from contents.models import Episode, Channel
from user_activities.models import Playlist, Like, Follow, Comment

from users.models import User


# Create your views here.

@method_decorator(login_required, name='dispatch')
class PlayListToAddView(mixins.ListModelMixin, ListView):
    context_object_name = 'objects'
    template_name = 'content_page.html'

    model = Playlist
    item_slug = ""
    item_type = ""

    def get_queryset(self):
        self.item_slug = self.kwargs['item_slug']
        self.item_type = self.kwargs['type']
        user = self.request.user
        return Playlist.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Playlist'
        context['icon'] = 'play'
        context['item_slug'] = self.item_slug
        context['item_type'] = self.item_type
        return context


@method_decorator(login_required, name='dispatch')
class AddToPlaylistView(View):
    def get(self, request, *args, **kwargs):
        playlist_id = self.kwargs.get('playlist_id')
        item_slug = self.kwargs.get('item_slug')
        item_type = self.kwargs.get('type')

        playlist = Playlist.objects.get(id=playlist_id)
        if item_type == 'episode':
            item = Episode.objects.get(slug=item_slug)
            playlist.episodes.add(item)

        playlist.save()

        return redirect(reverse('playlists_to_add', kwargs={'item_slug': item_slug, 'type': item_type}))


@login_required
def like_item(request, *args, **kwargs):
    user = request.user
    item = Episode.objects.get(id=kwargs['item_id'])

    like_record, state = Like.objects.get_or_create(user=user, item=item)
    if state:
        like_record.save()

    item.likes_count = Like.objects.filter(item=item).count()
    item.save()

    return HttpResponse('You have liked it')


@login_required
def unlike_item(request, *args, **kwargs):
    user = request.user
    item = Episode.objects.get(id=kwargs['item_id'])

    like_record, state = Like.objects.get_or_create(user=user, item=item)
    like_record.delete()

    item.likes_count = Like.objects.filter(item=item).count()
    item.save()

    return HttpResponse('You Unliked it')


@login_required
def follow_channel(request, *args, **kwargs):
    user = request.user
    item = Channel.objects.get(id=kwargs['item_id'])
    follow_record, state = Follow.objects.get_or_create(user=user, item=item)
    if state:
        follow_record.save()

    item.followers_count = Follow.objects.filter(item=item).count()

    item.save()

    return HttpResponse('Following')


@login_required
def unfollow_channel(request, *args, **kwargs):
    user = request.user
    item = Channel.objects.get(id=kwargs['item_id'])
    follow_record, state = Follow.objects.get_or_create(user=user, item=item)
    follow_record.delete()

    item.followers_count = Follow.objects.filter(item=item).count()

    item.save()

    return HttpResponse('UnFollowing')


@login_required
def send_comment(request):
    if request.user.is_authenticated:
        user = request.user
        item = Episode.objects.get(id=int(request.GET.get('episode_id')))
        comment_text = request.GET.get('comment_text')
        parent_id = request.GET.get('parent_id')
        parent_id = int(parent_id) if parent_id != "" else None
        print(user,item.slug,comment_text,parent_id)

        comment_record, state = Comment.objects.get_or_create(user=user, item=item, text=comment_text,
                                                              parent_id=parent_id)
        if state:
            comment_record.save()

        item.comments_count = Comment.objects.filter(item=item).count()
        item.provider.comments_count = Comment.objects.filter(item__provider=item.provider).count()

        item.provider.save()
        item.save()

    return HttpResponse('Send Comment')


@login_required
def delete_comment(request):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=int(request.GET.get('comment_id')))
        comment.delete()

    return HttpResponse('Delete Comment')
