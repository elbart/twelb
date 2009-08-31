from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^twelb/', include('twelb.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^frontend/$', 'twelb.frontend.views.index'),
    (r'^frontend/login/$', 'twelb.frontend.views.login'),
    (r'^frontend/dologin/$', 'twelb.frontend.views.dologin'),
    (r'^frontend/logout/$', 'twelb.frontend.views.logout'),
)
