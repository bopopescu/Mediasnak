import access_keys
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from random import randrange
from base64 import urlsafe_b64encode, b64encode
from datetime import datetime, timedelta
from msnak.s3util import hmac_sign
from models import MediaFile # Database table for files


def test_databases(request):

    set = request.GET['set']
    if set == 'true':
        f = MediaFile(file_id='testfileid', user_id=1, filename='testfilename',
        upload_time=datetime.utcnow(), view_count=0)#time.ctime #datetime.datetime
        f.save()
    
    retr = MediaFile.objects.all()[0]
    
    file_id = retr.file_id
    user_id = retr.user_id
    filename = retr.filename
    upload_time = retr.upload_time
    view_count = retr.view_count
    
    return render_to_response('test-databases.html', {'file_id':file_id,'user_id':user_id,'filename':filename,'upload_time':upload_time,'view_count':view_count})

def view_mediafile_model(request):

    retr = MediaFile.objects.all()
    
    # Could filter with the request's GET input

    
    # Multiple html repeats could be done with a template but I don't feel like
    # learning that at the moment
    content = '<html><head><title>MediaFile Table</title></head><body>';
    for r in retr:
      content += '''
        <div><pre>
        file_id------ '''+str(r.file_id)+'''
        user_id------ '''+str(r.user_id)+'''
        filename----- '''+str(r.filename)+'''
        upload_time-- '''+str(r.upload_time)+'''
        view_count--- '''+str(r.view_count)+'''
        </pre></div>
        '''
    content += '</body>';
    
    return HttpResponse(content)
    # return render_to_response('base.html', { 'title': 'Contents of the file database table', 'content': content }) # won't work, 'content' is a block, not a variable