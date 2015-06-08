from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blogengine.models import Post
# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'

class DetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
