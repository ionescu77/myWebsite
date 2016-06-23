from django.shortcuts import render
from django.views.generic import ListView, DetailView
# for code markdown
#from django.utils.encoding import force_str
#from django.utils.safestring import mark_safe
#import markdown2

from django.contrib.syndication.views import Feed

from blogengine.models import Post, Category, Tag

# Create your views here.
class CategoryListView(ListView):
    template_name = 'category_list.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            return Post.objects.filter(category=category)
        except Category.DoesNotExist:
            return Post.objects.none()                      # returns "No posts found"

class TagListView(ListView):
    template_name = 'tag_list.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            tag = Tag.objects.get(slug=slug)
            return tag.post_set.all()
        except Tag.DoesNotExist:
            return Post.objects.none()

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'

class DetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostsFeed(Feed):
    title = "ionescu77.com RSS feed - posts"
    link = "blog/feeds/posts/"
    description = "ionescu77.com RSS feed - blog posts"
    def items(self):
        return Post.objects.order_by('-pub_date')
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.text
