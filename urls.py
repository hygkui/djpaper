from django.conf.urls.defaults import *

from django.views.generic import list_detail
from django.conf import settings
from django.conf.urls.static import static
from views import * 
from books.views import search
from books.models import Publisher
from contact.views import contact,thanks
from djpaper.views import show_all_papers,show_departments,print_deps,show_paper_by_id,add_paper
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


pulisher_info = {
	'queryset':Publisher.objects.all(),
	'template_name':'publisher_list_page.html',
}

urlpatterns = patterns('',
    # Example:
    # (r'^djtest/', include('djtest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#	(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT, }),
#	(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT, }),
    (r'^admin/', include(admin.site.urls)),
	(r'^time/$',current_datetime),
	(r'^time/plus/(\d{1,2})/$',hours_ahead),
	(r'^meta/$',show_meta),
	(r'^search/$',search),
	(r'^contact/$',contact),
	(r'^contact/thanks/$',thanks),
	(r'^paper/$',show_all_papers),
	(r'^paper/(\d+)/$',show_paper_by_id),
	(r'^department/$',show_departments),
	(r'^paper/add/$',add_paper),
	(r'^publishers/$',list_detail.object_list,pulisher_info),
	(r'^about/$',about),
	
)

urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )

