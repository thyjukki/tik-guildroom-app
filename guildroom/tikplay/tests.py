"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase

from tikplay.youtube import get_id_from_url, NotYoutubeUrlException, NoIdYoutubeUrlException

# TODO: Configure your database in settings.py and sync before running tests.

class SimpleTest(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class YoutubeApi(TestCase):
    """Tests for the youtube api"""

    @classmethod
    def setUpClass(cls):
        django.setup()

    def test_id_from_url(self):
        id = get_id_from_url("https://www.youtube.com/watch?v=YE7VzlLtp-4")
        self.assertEqual(id, 'YE7VzlLtp-4', "Id does not match")
        
        short_id = get_id_from_url("https://youtu.be/YE7VzlLtp-4")
        self.assertEqual(short_id, 'YE7VzlLtp-4', "Short url id does not match")

        id = get_id_from_url("https://www.youtube.com/watch?v=YE7VzlLtp-4&t=179")
        self.assertEqual(id, 'YE7VzlLtp-4', "Url with time does not match")
        
        short_id = get_id_from_url("https://youtu.be/YE7VzlLtp-4?t=107")
        self.assertEqual(short_id, 'YE7VzlLtp-4', "Short url with time does not match")

        try:
            get_id_from_url("https://www.stackoverflow.com/watch?v=YE7VzlLtp-4")
            self.fail("Got id from a non youtube site")
        except NotYoutubeUrlException:
            pass

        try:
            get_id_from_url("https://www.youtube.com")
            self.fail("Got id from a non video page")
        except NoIdYoutubeUrlException:
            pass

        try:
            get_id_from_url("https://www.youtu.be")
            self.fail("Got id from a short non video page")
        except NoIdYoutubeUrlException:
            pass

