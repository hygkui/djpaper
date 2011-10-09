from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login
from views import about,show_meta,logout_page,current_datetime,hours_ahead,index
from contact.views import contact,thanks
from djpaper.views import show_all_papers,show_departments,print_deps,show_paper_by_id,\
				show_all_people,show_people_by_id,register,search_paper,show_paper_by_tag,\
				tag_add,paper_edit,pic_upload,abs_edit,author_add
from djpaper.ajax_utils import ajax_title_autocomplete
from djpaper.xls_utils import _xls_file_save,_xls_file_out_page
from djpaper.statistics import show_statistics,data_maker
# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()



from djpaper.feeds import *

feeds = {
	'recent':RecentPapers
}


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
	(r'^search/$',search_paper),
	(r'^contact/$',contact),
	(r'^contact/thanks/$',thanks),
	(r'^paper/$',show_all_papers),
	(r'^paper/(\d+)/$',show_paper_by_id),
	(r'^people/$',show_all_people),
	(r'^people/(\d+)/$',show_people_by_id),
	(r'^depart/$',show_departments),
	(r'^about/$',about),
   	(r'^index/$',index),
	(r'^$',index),
	(r'^accounts/login/$',login),
	(r'^accounts/logout/$',logout_page),
	(r'^accounts/register/$',register),
	(r'^accounts/profile/$',direct_to_template,{'template':'registration/welcome.html'}),
	(r'^register/success/$',direct_to_template,{'template':'registration/register_success.html'}),
	(r'^advance/$',direct_to_template,{'template':'advance.html'}),
	#for feeds 
	(r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed',{'feed_dict':feeds}),	
	#for tag-cloud
	(r'^tag/(\w+)/$',show_paper_by_tag),
	#for xls files read to save
	(r'^xls/in/$',_xls_file_save),
	(r'^xls/out/$',_xls_file_out_page),
	#for ajax
	(r'^ajax/title/autocomplete/$',ajax_title_autocomplete),
	#for search depart
	(r'^search/depart/$',show_statistics),
	#for statistic & st. is short for statistics
	(r'^st/depart/$',data_maker),
	# test for tag +
	(r'^tagadd/(\d+)$',tag_add),	
	# for paper edit 
	(r'^paper/edit/(\d+)$',paper_edit),	
	# for pic upload	
	(r'^pic/upload/(\d+)$',pic_upload),	
	# for abstract edit
	(r'^abs/edit/(\d+)$',abs_edit),	
	# for other author add.
	(r'^au/add/(\d+)$',author_add),	

)
#for static files
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )

