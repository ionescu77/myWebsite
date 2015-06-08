from django.conf.urls import patterns, url

from blogengine.views import PostListView

urlpatterns = [
    # Index Blog
    url(r'^(?P<page>\d+)?/?$', PostListView.as_view(paginate_by=3), name = 'post_list'),       # Generic ListView
]
