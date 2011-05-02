from django.conf.urls.defaults import *

from views import * 
from books.views import search
from contact.views import contact,thanks
from djpaper.views import show_all_papers,show_departments,print_deps,show_paper
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djtest/', include('djtest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
	(r'^time/$',current_datetime),
	(r'^time/plus/(\d{1,2})/$',hours_ahead),
	(r'^meta/$',show_meta),
	(r'^search/$',search),
	(r'^contact/$',contact),
	(r'^contact/thanks/$',thanks),
	(r'^paper/$',show_all_papers),
	(r'^department/$',show_departments),
	
)
