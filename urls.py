from django.conf.urls.defaults import *

from views import *
from books import views 
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
	(r'^search_form/$',views.search),
	(r'^search/$',views.search),
)
