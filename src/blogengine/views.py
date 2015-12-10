from django.shortcuts import render
from django.views.generic import ListView, DetailView
# for code markdown
#from django.utils.encoding import force_str
#from django.utils.safestring import mark_safe
#import markdown2

from blogengine.models import Post
# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'

class DetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
