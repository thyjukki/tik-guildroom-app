"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase

from tikplay.youtube import get_id_from_url, get_video, NotYoutubeUrlException, NoIdYoutubeUrlException, NoVideoYoutubeException

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
        except:
            self.fail("Wrong exception type")

        try:
            get_id_from_url("https://www.youtube.com")
            self.fail("Got id from a non video page")
        except NoIdYoutubeUrlException:
            pass
        except:
            self.fail("Wrong exception type")

        try:
            get_id_from_url("https://www.youtu.be")
            self.fail("Got id from a short non video page")
        except NoIdYoutubeUrlException:
            pass
        except:
            self.fail("Wrong exception type")

    def test_get_video(self):
        video = get_video("YE7VzlLtp-4")
        self.assertEqual(video.title, 'Big Buck Bunny', "Ttile does not match")
        self.assertEqual(video.description, "Big Buck Bunny tells the story of a giant rabbit with a heart bigger than himself. When one sunny day three rodents rudely harass him, something snaps... and the rabbit ain't no bunny anymore! In the typical cartoon tradition he prepares the nasty rodents a comical revenge.\r\n\r\nLicensed under the Creative Commons Attribution license\r\n\r\nhttp://www.bigbuckbunny.org/", "Description does not match")
        self.assertEqual(video.channel, 'Blender', "Channel does not match")
        self.assertEqual(video.image, 'https://i.ytimg.com/vi/YE7VzlLtp-4/maxresdefault.jpg', "Image url does not match")

        try:
            video_not = get_video("abla")
            self.fail("Found a video when with wrong id")
        except NoVideoYoutubeException:
            pass
        except:
            self.fail("Wrong exception type")