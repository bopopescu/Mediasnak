from django.utils.unittest import TestCase # This is django's copy of the unittest included in python 2.7
from django.test.client import Client
#from django.test import TestCase # Has stuff like assertContains, would like to use, but is giving errors when included

from msnak.models import MediaFile

class TestUpload(TestCase):
    fixtures = ['msnak_testfixture.json']

    def setUp(self):
        self.c = Client()

    # ACCEPTANCE CRITERIA, STORY 8
    def testPerformDownloadImage(self):
        pass
        
    # ACCEPTANCE CRITERIA, STORY 9
    def testPerformDownloadAudio(self):
        pass
        
    # ACCEPTANCE CRITERIA, STORY 10
    def testPerformDownloadVideo(self):
        pass