from django.shortcuts import render
from django.views.generic import ListView, DetailView
# for code markdown
#from django.utils.encoding import force_str
#from django.utils.safestring import mark_safe
#import markdown2

from blogengine.models import Post, Category

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

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'

class DetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
