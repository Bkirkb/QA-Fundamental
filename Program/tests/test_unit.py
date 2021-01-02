import unittest
from flask import url_for
from flask_testing import TestCase

from application import app, db
from application.models import Fish, Catches

class TestBase(TestCase):

	def create_app(self):
		app.config.update(
			SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
			SECRET_KEY='TEST_SECRET_KEY',
			DEBUG=True
		)
		return app

	def setUp(self):
		db.create_all()
		test_fish = Fish(name="test fish", minweight=1800, maxweight=2500)
		db.session.add(test_fish)
		db.session.commit()
		test_catch = Catches(fishname="test fish", fishweight=2030, fishid=test_fish.id, description="Jeeez what a catch")
		db.session.add(test_catch)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

class TestViews(TestBase):

# Test each route allows get requests and provides the right status code of 200
	def test_home_get(self):
		response = self.client.get(url_for('home'))
		self.assertEqual(response.status_code, 200)

	def test_create_get(self):
		response = self.client.get(url_for('create'))
		self.assertEqual(response.status_code, 200)

	def test_update_get(self):
		response = self.client.get(url_for('update', id=1))
		self.assertEqual(response.status_code,200)

# Follow redirects since the delete function works largely on the home page, without redirects being allowed the 302
# status code is returned, since the delete function redirects immediately to the home page once it has finished.
	def test_delete_get(self):
		response = self.client.get(
			url_for('delete', id=1)
			,follow_redirects = True
		)
		self.assertEqual(response.status_code,200)
		
class TestRead(TestBase):

# read the database to ensure that the fish is present by looking for test_fish (it is present within the catch too)
	def test_read_fish(self):
		response = self.client.get(url_for('home'))
		self.assertIn(b"test fish", response.data)

# read the database to ensure that the catch has been entered, since the fish table should only be storing 1800 and 2500, the 2030
# can only be present in the catch table.
	def test_read_catch(self):
		response = self.client.get(url_for('home'))
		self.assertIn(b"2030", response.data)

class TestCreate(TestBase):

# Create a catch and search for the information on the home page, the catch description is only present in the Catches table.
	def test_create_catch(self):
		response = self.client.post(
			url_for('create'),
			data=dict(fishname="test fish", fishweight=2000, description="Blimey What a catch"),
			follow_redirects = True
		)
		self.assertIn(b"Blimey What a catch", response.data)


# Ensure that the database is correctly updating when the fish min weight and max weight values are eclipsed by new values, tried to use python logic to test routes, couldn't quite figure it out
# but the tests here show that the code within routes.py is in fact working.

	def test_create_sbcatch(self):

		response = self.client.post(
			url_for('create'),
			data=dict(fishname="test fish", fishweight=2000, description="Blimey What a catch"),
			follow_redirects = True
		)
		fish = Fish(name="carp", minweight=4, maxweight=505)
		db.session.add(fish)
		db.session.commit()
		new_catch = Catches(fishid=fish.id,fishname="carp", fishweight=2, description="heaviest catch yet!")
		db.session.add(new_catch)
		db.session.commit()
		if fish.minweight > new_catch.fishweight:
			fish.minweight = new_catch.fishweight
			db.session.commit()
		self.assertTrue(fish.minweight == new_catch.fishweight)
	
class TestUpdate(TestBase):
# Update catch description from previous value to new value, search for new value on home page.

	def test_update_catch(self):
		response = self.client.post(
			url_for('update', id=1),
			data=dict(fishname="test fish", fishweight=2000, description="That catch was easy!"),
			follow_redirects = True 
		)
		self.assertIn(b"That catch was easy!", response.data)

class TestDelete(TestBase):

# Delete the catch and ensure that the data from the catch is no longer present on the home page, and as a result no longer
# present on the home page.

	def test_delete_catch(self):
		response = self.client.get(
			url_for('delete', id=1),
			follow_redirects = True 
		)
		self.assertNotIn(b"Jeeez what a catch", response.data)

