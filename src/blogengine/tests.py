from django.test import TestCase, LiveServerTestCase, Client

from django.utils import timezone
from blogengine.models import Post

# Create your tests here.
class PostTest(TestCase):
    def test_create_post(self):
      # Create the post
      post = Post()
      # Set the attributes
      post.title = 'My test post'
      post.text = 'This is my test blog post'
      post.pub_date = timezone.now()
      # Save it
      post.save()
      # Check if we can find it
      all_posts = Post.objects.all()
      self.assertEquals(len(all_posts), 1)
      only_post = all_posts[0]
      self.assertEquals(only_post, post)

      # Check attributes
      self.assertEquals(only_post.title, 'My test post')
      self.assertEquals(only_post.text, 'This is my test blog post')
      self.assertEquals(only_post.pub_date.day, post.pub_date.day)
      self.assertEquals(only_post.pub_date.month, post.pub_date.month)
      self.assertEquals(only_post.pub_date.year, post.pub_date.year)
      self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
      self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
      self.assertEquals(only_post.pub_date.second, post.pub_date.second)

class AdminTest(LiveServerTestCase):
    # We need to fill the auth database for login test
    # python manage.py dumpdata auth.User --indent=2 > blogengine/fixtures/users.json
    fixtures = ['users.json']

    def setUp(self):
        # Create client
        self.client = Client()

    def test_login(self):
        # Get login page
        response = self.client.get('/admin/', follow=True)
        # Check response code Django does redirect on Admin so code 302, we need to set follow=True
        self.assertEquals(response.status_code, 200)
        # Check 'Log in' in admin webpage
        self.assertTrue('Log in' in response.content)
        # Log the user in
        self.client.login(username='testuser', password="test")
        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        # Login
        self.client.login(username='testuser', password='test')
        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)
        # Log out
        self.client.logout()
        # Check response code
        response = self.client.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)
        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)

    # The admin interface implements URLs for creating new instances of a model in a consistent format of /admin/app_name/model_name/add/
    def test_create_admin_post(self):
        # Log in
        self.client.login(username='testuser', password='test')
        # Check 'Log in' in admin webpage
        response = self.client.get('/admin/')
        self.assertTrue('Log out' in response.content)
        # Check response code
        response = self.client.get('/admin/blogengine/post/add/', follow=True)
        self.assertEquals(response.status_code, 200)
        # Create the new post
        response = self.client.post('/admin/blogengine/post/add/', {
            'title': 'My first post',
            'text': 'This is my first post',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04'
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
        # Log in
        self.client.login(username='testuser', password='test')
        # Create the post
        blogpost = Post()
        blogpost.title = 'My editable post'
        blogpost.text = 'This is my first editable blog post'
        blogpost.pub_date = timezone.now()
        blogpost.save()
        # Edit the post
        response = self.client.post('/admin/blogengine/post/' + str(blogpost.pk) + '/', {
            'title': 'My EDITED post',
            'text': 'This is my EDITED editable blog post',
            'pub_date_0': '2015-05-28',
            'pub_date_1': '23:00:04',
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)
        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)
        # Check post amended
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post.title, 'My EDITED post')
        self.assertEquals(only_post.text, 'This is my EDITED editable blog post')

    def test_delete_post(self):
        # Create the post
        post = Post()
        post.title = 'My deletable post'
        post.text = 'This is my first deletable post'
        post.pub_date = timezone.now()
        post.save()
        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        # Log in
        self.client.login(username='testuser', password='test')
        # Delete the post
        response = self.client.post('/admin/blogengine/post/' + str(post.pk) + '/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        # Check if deleted successfully
        #print '%s' %response.content
        self.assertTrue('deleted successfully' in response.content)
        # Check post amended
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)

class PostViewTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        # Create the post
        post = Post()
        post.title = 'My first test post for View'
        post.text = 'This the first test post for view.'
        post.pub_date = timezone.now()
        post.save()
        # Check post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        # Fetch the index
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        # Check post title is in response
        self.assertTrue(post.title in response.content)
        # Check post text is in response
        self.assertTrue(post.text in response.content)
        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)
