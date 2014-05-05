__author__ = 'oskarmarszalek'

import os
import urllib2
from urlparse import urlparse
from celery import task
from django.core.files.base import ContentFile

from django.conf import settings
from .models import File

@task()
def Download_schedule_html():
    my_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                  'Accept-Encoding': 'none',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Connection': 'keep-alive'}
    html_file = File()
    try:
        file_url='http://wimii.pcz.pl/images/stories/plan_dzienny/Plan_dzienne_lato_grupy.html'
        html_file.file_name=urlparse(file_url).path.split('/')[-1]
        if os.path.exists(os.path.join(settings.MEDIA_ROOT+'/schedule_html', html_file.file_name)):
            import shutil, datetime
            shutil.move(os.path.join(settings.MEDIA_ROOT+'/schedule_html', html_file.file_name), os.path.join(settings.MEDIA_ROOT+'/archiwum_html'))
            os.rename(os.path.join(settings.MEDIA_ROOT+'/archiwum_html', html_file.file_name) , os.path.join(settings.MEDIA_ROOT+'/archiwum_html', datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S_")+html_file.file_name))
            html_file.save()

        req = urllib2.Request(file_url, headers=my_headers)
        content = ContentFile(urllib2.urlopen(req).read())
        html_file.file.save(html_file.file_name,content, save=True)
    except:
        html_file.delete()
