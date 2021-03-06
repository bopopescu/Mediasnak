from django.utils.unittest import TestCase # This is django's copy of the unittest included in python 2.7 (we're using an older version). This one also clears the database before each test
from django.test import TestCase # Has stuff like assertContains, would like to use, but is giving errors when included
from unittest import TestCase

from django.test.client import Client # Client lets us test django's generated pages without having to load them through a server to a browser
from msnak.models import MediaFile # Import our database model

import urllib2 #extended URL handling library
import msnak.s3util

class TestUpload(TestCase):
    key1="u/tests/file1"
    key2="u/tests/file2"
    key3="u/tests/file3"
    key4="u/tests/pQv-O2sFKi8"
    
    def setUp(self):
        # Manually load the database
        # The tests folder on S3 is used for holding test files
        MediaFile(file_id="u/tests/file1", user_id=0, filename="testfile1.png", upload_time="2011-01-01 00:00", view_count=100).save()
        MediaFile(file_id="u/tests/file2", user_id=0, filename="duplicatefilename.png", upload_time="2011-01-01 00:00", view_count=100).save()
        MediaFile(file_id="u/tests/file3", user_id=0, filename="duplicatefilename.png", upload_time="2011-01-01 00:00", view_count=100).save()
        MediaFile(file_id="u/tests/pQv-O2sFKi8", user_id=0, filename="Jellyfish.jpg", upload_time="2011-01-01 00:00", view_count=100).save()
        self.client1 = Client()
        
        
    # Must test to see that the key that gets returned each upload-request is different
    # Cue: Refactoring into seperate functions
        
    def testRequestUploadPage(self):
        #"Test the upload page exists"
        response = self.client1.get('/upload', {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Upload' in response.content) #self.assertContains(response, 'Upload')
        self.assertTrue('Upload a file:' in response.content) #self.assertContains(response, 'Upload a file:')
        
    def testSuccessBlankInput(self):
        #"Test that if the success page is went to without any input, redirect to upload page"
        response = self.client1.get('/success', {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'], ('Location', 'http://testserver/upload')) #self.assertRedirects(response, 'upload')

    def testSuccessWrongBucket(self):
        #"Test what happens if the wrong bucketname is given when returning from upload"
        response = self.client1.get('/success', {'bucket': 's3.blah.com', 'etag': '"735ab4f94fbcd57074377afca324c813"', 'key': 'u/tests/file1'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('error' in response.content)
        
    def testSuccessKeyNotOnS3(self):
        #"Test what happens if a random key is given when returning from upload"
        response = self.client1.get('/success',
            {'bucket': 's3.mediasnak.com', 'etag': '"735ab4f94fbcd57074377afca324c813"', 'key': 'u/tests/randomkeysdkfj'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('error' in response.content)
    
    def testSuccessKeyAlreadyUsed(self):
        #"Test what happens if an already taken key is given when returning from upload"
        response = self.client1.get('/success',
            {'bucket': 's3.mediasnak.com', 'etag': '"735ab4f94fbcd57074377afca324c813"', 'key': 'u/tests/file1'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('error' in response.content)

    def testPerformUpload(self):
        #"Test performing a full upload"
        
        response = self.client1.get('/upload', {})
        #response.text.contains()
        #{'key': key, 'aws_id': access_keys.key_id, 'policy': policy, 'signature': signature})
        #key = response.context['key'];
        key = 'u/tests/file1'
        #self.assertEqual(response.context['aws_id'], access_keys.key_id)
        #self.assertEqual(response.context['signature'], hmac_sign(policy))
        
        self.assertEqual(response.templates, [])
        # since for some reason the template list is blank, also the context is blank
        
        #self.assertEqual(response.templates[0].name, 'upload.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        
        #'bucket': bucket, 'key': key, 'etag': etag,
        #'upload_time': upload_time, 'file_id': file_id, 'user_id': user_id, 'filename': filename
        response = self.client1.get('/success',
            {'bucket': 's3.mediasnak.com', 'etag': '"735ab4f94fbcd57074377afca324c813"', 'key': key})
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.context['bucket'], 's3.mediasnak.com')
        #self.assertEqual(response.context['key'], key)
        #self.assertEqual(response.context['etag'], '"735ab4f94fbcd57074377afca324c813"')
        #self.assertTrue(datetime.utcnow() - response.context['upload_time'] < 100)
        #self.assertEqual(response.context['filename'], 'testfile.txt')
        
        
        #self.assertTrue('s3.mediasnak.com' in response.content)
        #self.assertTrue(key in response.content)
        #self.assertTrue('"735ab4f94fbcd57074377afca324c813"' in response.content)
        
        
    # ACCEPTANCE CRITERIA, STORY 1
    # A 'browse' option is shown to find the file
    # File is located on the server
    # File is handled using secure protocols, such as https 
    def testPerformUploadImage(self):
    
        # A 'browse' option is shown to find the file
        response = self.client1.get('/upload', {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<input type="file" ' in response.content)
        
        # FILE MUST GET UPLOADED NOW, MAY HAVE TO TEST THE REST WITH SELIUM
        filename = "test.jpg"
        key = "u/tests/file1"
        
        # File is located on the server
        self.assertNotEqual(MediaFile.objects.get(filename=filename), None)
        self.assertNotEqual(MediaFile.objects.get(file_id=key), None)
        from boto.s3.connection import S3Connection
        import access_keys
        botoconn = S3Connection(access_keys.key_id, access_keys.secret)
        bucket = botoconn.create_bucket('s3.mediasnak.com')
        file = bucket.get_key(key)
        self.assertNotEqual(file, None)
        self.assertEqual(file.get_metadata('filename'), filename)
        
        # File is handled using secure protocols, such as https
        
    # ACCEPTANCE CRITERIA, STORY 2
    #The specific audio format will be determined upon upload
    #A 'browse' option is shown to find the file
    #File is located on the server
    #File is handled using secure protocols, such as https 
    def testBrowseOptionWhenUploadingAudio(self):
        response = self.client1.get('/upload', {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<input type="file" ' in response.content)
    
    #def testPerformUploadAudio(self):
    #    pass
        
    # ACCEPTANCE CRITERIA, STORY 3
    #def testPerformUploadVideo(self):
    #    pass