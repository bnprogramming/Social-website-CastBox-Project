from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from contents.models import Channel
# from contents.models import Channel
from home_module.serializers import CountrySerializer
from utils.convertors import group_list


class HomeView(TemplateView):
    template_name = 'home_module/home_page.html'

    def get_context_data(self, **kwargs):

        context = super(HomeView, self).get_context_data(**kwargs)

        latest_episodes = Channel.get_new_items()

        most_popular_episodes = Channel.get_popular_items()

        most_followed_episodes = Channel.get_most_followed_items()

        context['latest_items'] = group_list(list(latest_episodes), 4)
        context['most_popular_items'] = group_list(list(most_popular_episodes), 4)
        context['most_followed_items'] = group_list(list(most_followed_episodes), 4)

        return context


@method_decorator(login_required, name='dispatch')
class CountryViewSetApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CountrySerializer


def site_header_partial(request):
    return render(request, 'shared/site_header_component.html')
