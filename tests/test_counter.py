"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""
# refactored code from prof
    def setUp(self):
        self.client = app.test_client()
        # name = 'CounterName'

# example 1
    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

# example 2
    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

# now we will create out own test called test_update_a_counter(self)
    def test_update_a_counter(self):
        # result should test the update method, first create a counter
        counter = app.test_client()
        basename = '/counters/foobar'
        result = counter.post(basename)
        # now test to make sure it was actually created
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # we already store a baseline for the counter
        base = result.get_json()['foobar']
        # basename = '/counters/foobar'
        # update the counter
        result = counter.put(basename)
        # now first test that it updated and assert they arent equal
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # to check the counter value is one more than the baseline we need to pull the new baseline and compare
        count = result.get_json()['foobar']
        self.assertEqual(base+1, count)

# for the read test we will create a counter and test the read function
    def test_read_a_counter(self):
        # create a test counter
        counter = app.test_client()
        # try to get counter name but no counter is there
        result = counter.get('/counters/supersecretsite')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        # now add the counter to the list of counters
        counter.post('/counters/supersecretsite')
        # now counter is made so test get success code
        result = counter.get('/counters/supersecretsite')
        self.assertEqual(result.status_code, status.HTTP_200_OK)

# create test case for delete function
    def test_delete_a_counter(self):
        # test deleting a name that does not exist
        counter = app.test_client
        result = counter.delete('/counters/deleteTest')
        # confirm deletion failed and counter should return a 404
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        # create counter
        counter.post('/counters/dontDeleteMe')
        # test deleting a name that is linked to a counter
        result = counter.delete('/counters/dontDeleteMe')
        # confirm counter got deleting
        self.assertEqual('/counters/dontDeleteMe')
