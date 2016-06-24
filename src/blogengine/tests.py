# This is for unicode characters in some unit tests:
# -*- coding: utf-8 -*-

from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.utils.encoding import smart_unicode

from django.test import TestCase, LiveServerTestCase, Client

from django.utils import timezone
from blogengine.models import Post, Category, Tag
import markdown2 as markdown
import feedparser

# Create your tests here.
class PostTest(TestCase):
    def test_create_category(self):
      # Create the category
      category = Category()
      # Add attributes
      category.name = 'python'
      category.description = 'Python the programming language'
      # Save it
      category.save()
      # Check if we can find it
      all_categories = Category.objects.all()
      self.assertEquals(len(all_categories), 1)
      only_category = all_categories[0]
      self.assertEquals(only_category, category)
      # Check attributes
      self.assertEquals(only_category.name, 'python')
      self.assertEquals(only_category.description, 'Python the programming language')

    def test_create_tag(self):
      # Create the tag
      tag = Tag()
      # Add attributes
      tag.name = 'pythonsky'
      tag.description = 'Pythonsky the programming language'
      # Save it
      tag.save()
      # Check if we can find it
      all_tags = Tag.objects.all()
      self.assertEquals(len(all_tags), 1)
      only_tag = all_tags[0]
      self.assertEquals(only_tag, tag)
      # Check attributes
      self.assertEquals(only_tag.name, 'pythonsky')
      self.assertEquals(only_tag.description, 'Pythonsky the programming language')

    def test_create_post(self):
      # Create the site
      site = Site()
      site.name = 'test.com'
      site.domain = 'test.com'
      site.save()

      # Create the category
      category = Category()
      category.name = 'python'
      category.description = 'Python the programming language'
      category.save()

      # Create the tag
      tag = Tag()
      tag.name = 'pythonsky'
      tag.description = 'Pythonsky the programming language'
      tag.save()

      # Create the post
      post = Post()
      # Set the attributes
      post.title = 'My test post'
      post.text = 'This is my test blog post'
      post.slug = 'my-test-post'
      post.pub_date = timezone.now()
      post.site = site
      post.category = category
      # Save it
      post.save()

      # Add the tag only after creating post
      post.tags.add(tag)
      post.save()

      # Check if we can find it
      all_posts = Post.objects.all()
      self.assertEquals(len(all_posts), 1)
      only_post = all_posts[0]
      self.assertEquals(only_post, post)

      # Check attributes
      self.assertEquals(only_post.title, 'My test post')
      #print '%s' %(only_post.text)
      self.assertEquals(only_post.text, 'This is my test blog post')
      self.assertEquals(only_post.slug, 'my-test-post')
      self.assertEquals(only_post.pub_date.day, post.pub_date.day)
      self.assertEquals(only_post.pub_date.month, post.pub_date.month)
      self.assertEquals(only_post.pub_date.year, post.pub_date.year)
      self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
      self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
      self.assertEquals(only_post.pub_date.second, post.pub_date.second)
      self.assertEquals(only_post.site.name, 'test.com')
      self.assertEquals(only_post.site.domain, 'test.com')
      self.assertEquals(only_post.category.name, 'python')
      self.assertEquals(only_post.category.description, 'Python the programming language')

      # Check tags
      post_tags = only_post.tags.all()
      self.assertEquals(len(post_tags), 1)
      only_post_tag = post_tags[0]
      self.assertEquals(only_post_tag, tag)
      self.assertEquals(only_post_tag.name, 'pythonsky')
      self.assertEquals(only_post_tag.description, 'Pythonsky the programming language')

    def test_create_romanian_post(self):
      # Create the site
      site = Site()
      site.name = 'test.com'
      site.domain = 'test.com'
      site.save()
      # Create the tag
      tag = Tag()
      tag.name = u'răzvansky'
      tag.description = u'Răzvan the programming language'
      tag.save()
      # Create the post
      post = Post()
      # Set attributes including romanian characters "diacritice"
      post.title = 'Testul cu șțăîâ'
      post.text = 'Ăsta este textul de test cu ăîșțâ'
      post.slug = 'testul-cu-staia'      # testing prepopulated fields in admin is out of scope now. So we pass.
      post.pub_date = timezone.now()
      post.site = site
      post.save()
      # Add the tag only after creating post
      post.tags.add(tag)
      post.save()
      # Check if we can find it
      all_posts = Post.objects.all()
      self.assertEquals(len(all_posts), 1)
      only_post = all_posts[0]
      self.assertEquals(only_post, post)

      # Check attributes
      self.assertEquals(only_post.title, u'Testul cu șțăîâ')
      print '%s' %(only_post.text)
      self.assertEquals(only_post.text, u'Ăsta este textul de test cu ăîșțâ')
      self.assertEquals(only_post.slug, 'testul-cu-staia')
      self.assertEquals(only_post.pub_date.day, post.pub_date.day)
      self.assertEquals(only_post.pub_date.month, post.pub_date.month)
      self.assertEquals(only_post.pub_date.year, post.pub_date.year)
      self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
      self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
      self.assertEquals(only_post.pub_date.second, post.pub_date.second)

      # Check tags
      post_tags = only_post.tags.all()
      self.assertEquals(len(post_tags), 1)
      only_post_tag = post_tags[0]
      self.assertEquals(only_post_tag, tag)
      self.assertEquals(only_post_tag.name, u'răzvansky')
      self.assertEquals(only_post_tag.description, u'Răzvan the programming language')

class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

class AdminTest(BaseAcceptanceTest):
    # We need to fill the auth database for login test
    # python manage.py dumpdata auth.User --indent=2 > blogengine/fixtures/users.json
    fixtures = ['users.json']

    def setUp(self):
        # Create client
        self.client = Client()

    def test_login(self):
        # Get login page
        response = self.client.get('/administrare/', follow=True)
        # Check response code Django does redirect on Admin so code 302, we need to set follow=True
        self.assertEquals(response.status_code, 200)
        # Check 'Log in' in admin webpage
        self.assertTrue('Log in' in response.content)
        # Log the user in
        self.client.login(username='testuser', password="test")
        # Check response code
        response = self.client.get('/administrare/')
        self.assertEquals(response.status_code, 200)
        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        # Login
        self.client.login(username='testuser', password='test')
        # Check response code
        response = self.client.get('/administrare/')
        self.assertEquals(response.status_code, 200)
        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)
        # Log out
        self.client.logout()
        # Check response code
        response = self.client.get('/administrare/', follow=True)
        self.assertEquals(response.status_code, 200)
        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)

    # The admin interface implements URLs for creating new instances of a model in a consistent format of /administrare/app_name/model_name/add/
    def test_create_category(self):
        # Log in
        self.client.login(username='testuser', password="test")
        # Check response code
        response = self.client.get('/administrare/blogengine/category/add/')
        self.assertEquals(response.status_code, 200)
        # Create the new category
        response = self.client.post('/administrare/blogengine/category/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        # Check added successfully
        self.assertTrue('added successfully' in response.content)
        # Check new category now in database
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
    def test_edit_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        # Log in
        self.client.login(username='testuser', password="test")
        # Edit the category
        response = self.client.post('/administrare/blogengine/category/' + str(category.pk) + '/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)
        self.assertEquals(response.status_code, 200)
        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)
        # Check category amended
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category.name, 'perl')
        self.assertEquals(only_category.description, 'The Perl programming language')
    def test_delete_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        # Log in
        self.client.login(username='testuser', password="test")
        # Delete the category
        response = self.client.post('/administrare/blogengine/category/' + str(category.pk) + '/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)
        # Check category deleted
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 0)

    def test_create_tag(self):
        # Log in
        self.client.login(username='testuser', password='test')
        # Check response code
        response = self.client.get('/administrare/blogengine/tag/add/')
        self.assertEquals(response.status_code, 200)
        # Create the new tag
        response = self.client.post('/administrare/blogengine/tag/add/', {
            'name': 'pythonsky',
            'description': 'The Pythonsky programming language'
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        # Check added successfully
        self.assertTrue('added successfully' in response.content)
        # Check new tag now in database
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 1)
    def test_edit_tag(self):
        # Create the tag
        tag = Tag()
        tag.name = 'pythonsky'
        tag.description = 'The Pythonsky programming language'
        tag.save()
        # Log in
        self.client.login(username='testuser', password='test')
        # Edit the tag
        response = self.client.post('/administrare/blogengine/tag/' + str(tag.pk) + '/', {
            'name': 'perlsky',
            'description': 'The Perlsky programming language'
            }, follow=True)
        self.assertEquals(response.status_code, 200)
        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)
        # Check tag amended
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 1)
        only_tag = all_tags[0]
        self.assertEquals(only_tag.name, 'perlsky')
        self.assertEquals(only_tag.description, 'The Perlsky programming language')
    def test_delete_tag(self):
        # Create the tag
        tag = Tag()
        tag.name = 'python'
        tag.description = 'The Python programming language'
        tag.save()
        # Log in
        self.client.login(username='testuser', password='test')
        # Delete the tag
        response = self.client.post('/administrare/blogengine/tag/' + str(tag.pk) + '/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)
        # Check tag deleted
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 0)


    def test_create_admin_post(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'pythonsky'
        tag.description = 'The Pythonsky programming language'
        tag.save()

        # Log in
        self.client.login(username='testuser', password='test')
        # Check 'Log in' in admin webpage
        response = self.client.get('/administrare/')
        self.assertTrue('Log out' in response.content)
        # Check response code
        response = self.client.get('/administrare/blogengine/post/add/', follow=True)
        self.assertEquals(response.status_code, 200)
        # Create the new post
        response = self.client.post('/administrare/blogengine/post/add/', {
            'title': 'My first post',
            'text': 'This is my first post',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04',
            'slug': 'my-first-post',
            'site': '1',
            'category': str(category.pk),
            'tags': str(tag.pk)
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)
        # Check added successfully
        #self.assertTrue('added successfully' in response.content)  # Somehow this does not work, is AJAX or smthing???!!
        # in fact the password was wrong and we were not logged in
        self.assertTrue('added successfully' in response.content)
        # Check new post now in database
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

    def test_edit_post(self):
        # Create the site
        site = Site()
        site.name = 'edit.com'
        site.domain = 'edit.com'
        site.save()

        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'pythonsky'
        tag.description = 'The Pythonsky programming language'
        tag.save()

        # Log in
        self.client.login(username='testuser', password='test')
        # Create the post
        blogpost = Post()
        blogpost.title = 'My editable post'
        blogpost.text = 'This is my first editable blog post'
        blogpost.slug = 'my-editable-post'
        blogpost.pub_date = timezone.now()
        blogpost.site = site
        blogpost.save()
        # Edit the post
        response = self.client.post('/administrare/blogengine/post/' + str(blogpost.pk) + '/', {
            'title': 'My EDITED post',
            'text': 'This is my EDITED editable blog post',
            'pub_date_0': '2015-05-28',
            'pub_date_1': '23:00:04',
            'slug': 'my-edited-post',
            'site': '1',
            'category': str(category.pk),
            'tags': str(tag.pk)
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)
        # Check changed successfully
        # print '%s' %category.pk
        self.assertTrue('changed successfully' in response.content)
        # Check post amended
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post.title, 'My EDITED post')
        self.assertEquals(only_post.text, 'This is my EDITED editable blog post')

    def test_delete_post(self):
        # Create the site
        site = Site()
        site.name = 'delete.com'
        site.domain = 'delete.com'
        site.save()

        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'pythonsky'
        tag.description = 'The Pythonsky programming language'
        tag.save()

        # Create the post
        post = Post()
        post.title = 'My deletable post'
        post.text = 'This is my first deletable post'
        post.slug = 'my-deletable-post'
        post.pub_date = timezone.now()
        post.site = site
        post.category = category
        post.save()
        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        # Log in
        self.client.login(username='testuser', password='test')
        # Delete the post
        response = self.client.post('/administrare/blogengine/post/' + str(post.pk) + '/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        # Check if deleted successfully
        #print '%s' %response.content
        self.assertTrue('deleted successfully' in response.content)
        # Check post deleted
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)

class PostViewTest(BaseAcceptanceTest):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        # Create the site
        site = Site()
        site.name = 'test.com'
        site.domain = 'test.com'
        site.save()

        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'pythonsky'
        tag.description = 'The Pythonsky programming language'
        tag.save()

        # Create the post
        post = Post()
        post.title = 'My first test post for View'
        post.text = 'This the first test post for view. And [markdown blog](http://127.0.0.1:8000/)'
        post.slug = 'my-first-test-post-for-view'
        post.pub_date = timezone.now()
        post.site = site
        post.category = category
        post.save()
        post.tags.add(tag)
        # Check post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        # Fetch the index
        response = self.client.get('/blog/')
        self.assertEquals(response.status_code, 200)
        # Check post title is in response
        #print "%s" %response
        self.assertTrue(post.title in response.content)
        # Check post text is in response
        #print "%s" %response
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))
        # Check the post category is in the response
        self.assertTrue(post.category.name in response.content)
        # Check the post tag is in the response
        post_tag = all_posts[0].tags.all()[0]
        self.assertTrue(post_tag.name in response.content.decode('utf-8'))
        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)
        # Check if link is marked-up properly by markdown
        #print "%s" %response.content
        # need to add something like
        # <a href="/blog/2015/7/my-first-test-post-for-view/">My first test post for View</a>
        #
        self.assertTrue('<a href="http://127.0.0.1:8000/">markdown blog</a>' in response.content)

    def test_post_page(self):
        # Create the site
        site = Site()
        site.name = 'test.com'
        site.domain = 'test.com'
        site.save()
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        # Create the tag
        tag = Tag()
        tag.name = 'pythonsky'
        tag.description = 'The Pythonsky programming language'
        tag.save()
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.site = site
        post.category = category
        post.save()
        post.tags.add(tag)
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the post URL
        post_url = only_post.get_absolute_url()
        #print "%s" %post_url

        # Fetch the post
        response = self.client.get("%s" %post_url)
        self.assertEquals(response.status_code, 200)
        #print "%s" %response

        # Check the post title is in the response
        self.assertTrue(post.title in response.content)

        # Check the post category is in the response
        self.assertTrue(post.category.name in response.content)

        # Check the post category is in the response
        post_tag = all_posts[0].tags.all()[0]
        self.assertTrue(post_tag.name in response.content.decode('utf-8'))

        # Check post text is in response, will fail with markdown unless UTF8 decode
        #self.assertTrue(post.text in response.content)
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))

        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_category_page(self):
        # Create the site
        site = Site()
        site.name = 'test.com'
        site.domain = 'test.com'
        site.save()
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.site = site
        post.category = category
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)
        # Get the category URL
        category_url = post.category.get_absolute_url()
        # Fetch the non-existing category to test view exception
        response = self.client.get("/blog/category/non-existing")
        self.assertEqual(response.status_code, 200)
        # Check empty querySet objects.none() - returns "No posts found"
        self.assertTrue('no posts found' in response.content.decode('utf-8'))
        # Fetch the category
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        # Check the category name is in the response
        self.assertTrue(post.category.name in response.content.decode('utf-8'))
        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))
        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content.decode('utf-8'))
        self.assertTrue(post.pub_date.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(post.pub_date.day) in response.content.decode('utf-8'))
        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content.decode('utf-8'))
        # Check the correct template was used
        self.assertTemplateUsed(response, 'category_list.html')

    def test_tag_page(self):
        # Create the site
        site = Site()
        site.name = 'test.com'
        site.domain = 'test.com'
        site.save()
        # Create the tag
        tag = Tag()
        tag.name = 'pythonsky'
        tag.description = 'The Pythonsky programming language'
        tag.save()
        # Create the post
        post = Post()
        post.title = 'My tagged post'
        post.text = 'This is [my tagged blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-tagged-post'
        post.pub_date = timezone.now()
        post.site = site
        post.save()
        post.tags.add(tag)
        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)
        # Get the tag URL
        tag_url = post.tags.all()[0].get_absolute_url()
        # Fetch the non-existing tag to test view exception
        response = self.client.get("/blog/tag/non-existing")
        self.assertEqual(response.status_code, 200)
        # Check empty querySet objects.none() - returns "No posts found"
        self.assertTrue('no coresponding posts found' in response.content.decode('utf-8'))

        # Fetch the tag
        response = self.client.get(tag_url)
        self.assertEquals(response.status_code, 200)
        # Check the tag name is in the response
        self.assertTrue(post.tags.all()[0].name in response.content.decode('utf-8'))
        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))
        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)
        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my tagged blog post</a>' in response.content)

# TEST for FLATPAGES Section
class FlatPageViewTest(BaseAcceptanceTest):
    def test_create_flatpage(self):
        # Create FlatPage
        page = FlatPage()
        page.url = '/about/'
        page.title = 'About Me'
        page.content = 'All about me. Well almost ...'
        page.save()

        # Add the site
        page.sites.add(Site.objects.all()[0])
        page.save()

        # Check new page saved
        all_pages = FlatPage.objects.all()
        self.assertEquals(len(all_pages), 1)
        only_page = all_pages[0]
        self.assertEquals(only_page, page)

        # Check data correct
        self.assertEquals(only_page.url, '/about/')
        self.assertEquals(only_page.title, 'About Me')
        self.assertEquals(only_page.content, 'All about me. Well almost ...')

        # Get URL
        page_url = only_page.get_absolute_url()

        # Get the page
        response = self.client.get(page_url)
        self.assertEquals(response.status_code, 200)

        # Get title and content in the response
        self.assertTrue('About Me' in response.content)
        self.assertTrue('All about me. Well almost ...' in response.content)

# TEST for RSS Feeds
class FeedTest(BaseAcceptanceTest):
    def test_all_post_feed(self):
        # Create the site
        site = Site()
        site.name = 'test.com'
        site.domain = 'test.com'
        site.save()
        # Create the category
        category = Category()
        category.name = 'pythonsky'
        category.description = 'The pythonic programming language'
        category.save()
        #Create the tag
        tag = Tag()
        tag.name = 'python'
        tag.description = 'The python programming language'
        tag.save()
        # Create a post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.site = site
        post.category = category
        # Save it
        post.save()
        # Add the tag
        post.tags.add(tag)
        post.save()
        # Check we can find it
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Fetch the feed
        response = self.client.get('/blog/feeds/posts/')
        self.assertEquals(response.status_code, 200)
        # Parse the feed
        feed = feedparser.parse(response.content)
        # Check length
        self.assertEquals(len(feed.entries), 1)
        # Check post retrieved is the correct one
        feed_post = feed.entries[0]
        self.assertEquals(feed_post.title, post.title)
        self.assertEquals(feed_post.description, post.text)
