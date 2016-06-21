from django.conf.urls import patterns, url
from blogengine.models import Post, Category
from blogengine.views import PostListView, DetailView, CategoryListView

urlpatterns = [
    # Index Blog
    url(r'^(?P<page>\d+)?/?$',
     PostListView.as_view(
        paginate_by=7
        ), name = 'post_list'),       # Generic ListView

    # Individual posts
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$',
     DetailView.as_view()),

    # Categories
    url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$',
     CategoryListView.as_view(
        paginate_by=5,
        model=Category,
        )),
]
