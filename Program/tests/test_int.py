import unittest
import time
from flask import  url_for
from urllib.request import urlopen

from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from application import app, db
from application.models import Fish, Catches

class TestBase(LiveServerTestCase):

    def create_app(self):
        #Configure the flask app before every test

        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
        app.config['SECRET_KEY'] = "adasdasfasfsdsdfsdfsd"
        return app
    
    def setUp(self):
        #Setup the test driver and create the table schema before every test. Populate the table
        # with a fish and a catch.

        print("------------------------------NEXT-TEST---------------------------")
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/chromium-browser"
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path="/home/home/chromedriver", chrome_options=chrome_options)
        self.driver.get("http://localhost:5000")
        db.drop_all()
        db.create_all()

        test_fish = Fish(name="test fish", minweight=500, maxweight=2000)
        db.session.add(test_fish)
        db.session.commit()
        test_catch = Catches(fishname=test_fish.name, fishid=test_fish.id, fishweight=1400, description="this is a test fish")
        db.session.add(test_catch)
        db.session.commit()

    def tearDown(self):
        #Stop the driver after every test

        self.driver.quit()
        print("------------------------------END-OF-TEST---------------------------\n\n\n---------------------------")

    def test_server_is_up_and_running(self):
        #Test that the server is running before each test.

        response = urlopen("http://localhost:5000")
        self.assertEqual(response.code, 200)


class TestCatchCreation(TestBase):
        #Test that the user can navigate to the create catch page, enter details and check to see if it
        #redirects to the home page.

    def test_catch_creation(self):

        #Navigate to the Create Catch page
        self.driver.find_element_by_xpath('/html/body/nav/li[2]/a').click()
        time.sleep(1)

        #Input the details in the form fields
        self.driver.find_element_by_xpath('//*[@id="name"]').send_keys("test fish")
        self.driver.find_element_by_xpath('//*[@id="weight"]').send_keys("1600")
        self.driver.find_element_by_xpath('//*[@id="description"]').send_keys("Fun_Catch")
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        # Assert that browser redirects to the home page
        assert url_for('home') in self.driver.current_url
        assert Catches.query.filter_by(id=2).first().description == "fun_catch"


class TestCatchUpdate(TestBase):

    def test_catch_update(self):

        #Navigate to the update page

        self.driver.find_element_by_xpath('//*[@id="div1"]/form[1]/input').click()
        time.sleep(1)

        # Update description for catch
        self.driver.find_element_by_xpath('//*[@id="description"]').send_keys("This is a new test description")
        self.driver.find_element_by_xpath('//*[@id="submit2"]').click()
        time.sleep(1)

        # Assert that the user is redirected to the home page
        assert url_for('home') in self.driver.current_url
        # Assert that the new update is present in the page
        assert Catches.query.filter_by(id=1).first().description == "This is a new test description"


class TestCatchDeletion(TestBase):
    #Test that the user can delete a catch from the home page and that it automatically redirects to the home page

    def test_catch_deletion(self):

        #Click the delete button
        self.driver.find_element_by_xpath('//*[@id="div1"]/form[2]/input').click()
        time.sleep(1)

        # Assert that browser redirects to the home page
        assert url_for('home') in self.driver.current_url
        # Assert that catch is no longer on page
        assert Catches.query.filter_by(id=1).first() == None

if __name__ =='__main__':
    unittest.main(port=5000)


                
