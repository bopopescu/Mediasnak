from django.utils.unittest import TestCase # This is django's copy of the unittest included in python 2.7 (we're using an older version). This one also clears the database before each test
from django.test import TestCase # Has stuff like assertContains, would like to use, but is giving errors when included
from unittest import TestCase

from django.test.client import Client # Client lets us test django's generated pages without having to load them through a server to a browser
from msnak.models import MediaFile # Import our database model

import urllib2 #extended URL handling library
import msnak.s3util

class TestDownload(TestCase):
    # A 'download' option is shown to find the directory to put the file
    # File is located on my computer or portable device
    # ACCEPTANCE CRITERIA, STORY 8
    def testDownloadOptionWhenDownloadingImage(self):
        response = self.client1.get('/file-details', {'fileid': 'tests/file1'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<a ' in response.content)
        self.assertTrue('download' in response.content)
        
        
    def testPerformDownloadImage(self):
        bucketname = "s3.mediasnak.com"
        key = "u/tests/file1"
        url = s3util.sign_url(bucketname, key)
        
        page = urllib2.urlopen(url)
        output = open("testimage.jpg", "wb")
        output.write(page.read())
        output.close()

        size = os.path.getsize("testimage.jpg")
        self.assertTrue(size > 0)
        
    # ACCEPTANCE CRITERIA, STORY 9
    #def testPerformDownloadAudio(self):
    #    pass
        
    # ACCEPTANCE CRITERIA, STORY 10
    #def testPerformDownloadVideo(self):
    #    pass
    #File's name should be displayed on the page
    def testFileNameWhenViewingVideo(self):
        response = self.client1.get('/file-details', {'fileid': 'u/tests/videofile1'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<video1s filename>' in response.content)