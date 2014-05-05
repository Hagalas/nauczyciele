from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from lista.api import TeacherResource

teacher_resource = TeacherResource()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nauczyciele.views.home', name='home'),
    # url(r'^nauczyciele/', include('nauczyciele.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^download-teachers/$', 'downloader.views.download_teachers', name='download_teachers'),
    url(r'^api/', include(teacher_resource.urls)),

    url(r'^test/$', 'downloader.views.test', name='test'),
)
