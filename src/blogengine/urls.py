from django.conf.urls import patterns, url

from blogengine.views import PostListView

urlpatterns = [
    # Index Blog
    url(r'^$', PostListView.as_view(), name = 'post_list'),       # Generic ListView
]
