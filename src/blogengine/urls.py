from django.conf.urls import patterns, url

from blogengine.views import PostListView, DetailView

urlpatterns = [
    # Index Blog
    url(r'^(?P<page>\d+)?/?$', PostListView.as_view(paginate_by=3), name = 'post_list'),       # Generic ListView
    # Individual posts
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view()),
]
