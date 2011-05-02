from django.http import HttpResponse
import datetime
# import template system
#from django.template.loader import get_template
#from django.template import Context

# import shortcuts
from django.shortcuts import render_to_response #there is no need to import template modules. this module is emough!

def current_datetime(request):
	now = datetime.datetime.now()
	return render_to_response('current_datetime_use_base.html',{'c_date':now})	


def hours_ahead(request,offset):
	offset = int (offset)
	dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
	html = "<html><body> In %s hour(s), it will be %s </body></html>" % (offset , dt)
	return HttpResponse(html)

def show_meta(request):
	values = request.META.items()
	values.sort()
	return render_to_response('show_meta.html',{'values':values})
	
