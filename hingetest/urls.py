from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'codingexercise.views.index'),
    url(r'^register$', 'codingexercise.views.register'),
    url(r'^friends$', 'codingexercise.views.friends'),
)
