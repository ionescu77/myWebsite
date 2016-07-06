"""ionescu77Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from django.contrib.flatpages import views

from django.contrib.sitemaps.views import sitemap
from blogengine.sitemap import PostSitemap, FlatpageSitemap

sitemaps = {
    'posts': PostSitemap,
    'pages': FlatpageSitemap
}

admin.autodiscover()

urlpatterns = [
    url(r'^administrare/', include(admin.site.urls)),

    # Blogengine URLs
    url(r'^blog/', include('blogengine.urls')),

    # Landing page URLs
    url(r'^$', include('landing.urls')),

    # Create sitemaps.xml
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # FlatPage URLs
    # url(r'^$', include('django.contrib.flatpages.urls')), # this or catchall does not really work
    url(r'^about/$', views.flatpage, {'url': '/about/'}, name='about'),

]
