from django.db import models
from django.utils.text import slugify
from django.contrib.sites.models import Site

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Category, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return "/blog/category/%s/" % (self.slug)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'categories'

class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Tag, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return "/blog/tag/%s/" % (self.slug)
    def __unicode__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    text = models.TextField()
    slug = models.SlugField(max_length=40, unique=True)
    site = models.ForeignKey(Site)
    category = models.ForeignKey(Category, blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    def get_absolute_url(self):
        return "/blog/%s/%s/%s/" % (self.pub_date.year, self.pub_date.month, self.slug)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-pub_date"]
