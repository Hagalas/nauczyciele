import os
import re
import urllib2
from urlparse import urlparse
from django.http import HttpResponse
from django.core.files.base import ContentFile
from bs4 import BeautifulSoup

from django.conf import settings
from .models import File
from lista.models import Teacher


def test(request):
    response = HttpResponse('Test00')

    teachers_pattern_results = []
    teachers_list = []
    text = []
    latest_file = File.objects.latest('addition_time')

    with open(str(latest_file.file.file)) as html_doc:
        soup = BeautifulSoup(html_doc)
        teachers_pattern = \
            re.compile(r'^(\w*-{0,1}\w+)\s{1}(\w+.?)\s{1,2}(\w+.?\s*\w*.?\s{0,1}\w*.?\s*\w*.?\s*\w*.?\s*\w*.?\s*\w*.?)\s*/{1}(\w*)/{1}$', re.UNICODE)
        a_hrefs = [link for link in soup.find_all('a') if link.get_text() != '']
        for link in a_hrefs:
            text.append(link.get_text())
            teachers_list.append(Teacher())

        for index, t in enumerate(text):
            teachers_pattern_results.append(re.findall(teachers_pattern, text[index])[0])

        for index, t in enumerate(teachers_list):
            teachers_list[index].surname = teachers_pattern_results[index][0]
            teachers_list[index].name = teachers_pattern_results[index][1]
            teachers_list[index].degree = teachers_pattern_results[index][2]
            teachers_list[index].faculty = teachers_pattern_results[index][3]
            teachers_list[index].save()

    return response


def download_teachers(request):
    """Creates teachers: their name, surname, degree and faculty"""
    my_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                  'Accept-Encoding': 'none',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Connection': 'keep-alive'}

    # gets file from 'file_url' below
    file_url = 'http://wimii.pcz.pl/download/plan_stacjonarny/Plan_dzienne_lato_13_14_3_nauczyciel.html'
    req = urllib2.Request(file_url, headers=my_headers)
    content = ContentFile(urllib2.urlopen(req).read())

    html_file = File()

    latest_dir = os.path.join(settings.MEDIA_ROOT, 'latest')
    archive_dir = os.path.join(settings.MEDIA_ROOT, 'archive')
    try:
        html_file.file_name = urlparse(file_url).path.split('/')[-1]
        if os.path.exists(os.path.join(latest_dir, html_file.file_name)):
            import shutil
            import datetime
            new_file_name = \
                os.path.join(archive_dir, datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S_")+html_file.file_name)
            shutil.move(os.path.join(latest_dir, html_file.file_name), new_file_name)

            html_file.save()

        html_file.file.save(html_file.file_name, content, save=True)
        response = HttpResponse('Pobrano plik: %s .' % html_file.file_name)
    except:
        html_file.delete()
        response = HttpResponse('Error')

    teachers_pattern_results = []
    teachers_list = []
    text = []
    latest_file = File.objects.latest('addition_time')
    with open(str(latest_file.file.file)) as html_doc:
        soup = BeautifulSoup(html_doc)
        teachers_pattern = \
            re.compile\
            (r'^(\w*-{0,1}\w+)\s{1}(\w+.?)\s{1,2}(\w+.?\s*\w*.?\s{0,1}\w*.?\s*\w*.?\s*\w*.?\s*\w*.?\s*\w*.?)\s*/{1}(\w*)/{1}$',\
             re.UNICODE)

        a_hrefs = [link for link in soup.find_all('a') if link.get_text() != '']

        for link in a_hrefs:
            text.append(link.get_text())
            teachers_list.append(Teacher())

        for index, t in enumerate(text):
            teachers_pattern_results.append(re.findall(teachers_pattern, text[index])[0])

        for index, t in enumerate(teachers_list):
            teachers_list[index].surname = teachers_pattern_results[index][0]
            teachers_list[index].name = teachers_pattern_results[index][1]
            teachers_list[index].degree = teachers_pattern_results[index][2]
            teachers_list[index].faculty = teachers_pattern_results[index][3]
            teachers_list[index].save()

    return response