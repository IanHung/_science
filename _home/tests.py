"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from _home.views import home
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
class HomePageTest(TestCase):
    
    #Can we resolve the URL /
    # Can we make this view return the desired html content
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)
        
    def test_home_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('_home/home.html')
        self.assertEqual(response.content.decode(), expected_html)


        
    