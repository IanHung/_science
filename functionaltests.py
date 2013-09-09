'''
Created on 2013-09-04

@author: Ian
'''
import unittest
from selenium import webdriver

class HomeFunctionTest(unittest.TestCase):
    
    #setup runs at the start of a functional test
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
        
    def test_homepage_load(self):
        #Felicity Archer has heard about a cool new online labbook app. She goes
        #to check out its homepage
        self.browser.get('http://localhost:8000')
        
        #She notices the page title and header mentions _science 
        self.assertIn('_Science', self.browser.title)
        
    def test_aboutpage_load(self):
        #Felicity Archer wants to find out more about this project.
        #She visits the about page.
        #There she sees a title and a brief introduction
        self.browser.get('http://localhost:8000/about')
        
if __name__ == '__main__':
    unittest.main()