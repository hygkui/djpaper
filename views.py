from django.http import HttpResponse
import datetime
# import template system
#from django.template.loader import get_template
#from django.template import Context

# import shortcuts
from django.shortcuts import render_to_response #there is no need to import template modules. this module is emough!

##old 
#def current_datetime(request):
#	now = datetime.datetime.now()
#	html = "<html><body> It is now %s </body></html>" % now
#	return HttpResponse(html)

#new : too much need to import template system as get_template && Context
#def current_datetime(request):
#	now = datetime.datetime.now()
#	t = get_template( 'current_datetime.html')	
#	html = t.render( Context ( { 'c_date':now } ) )
#	return HttpResponse(html)

#new : use django.shortcuts. render_to_response()
# need to import shortcuts modules 
def current_datetime(request):
	now = datetime.datetime.now()
#	return render_to_response('current_datetime.html',{'c_date':now})	
	return render_to_response('current_datetime_use_base.html',{'c_date':now})	







def hours_ahead(request,offset):
	offset = int (offset)
	dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
	html = "<html><body> In %s hour(s), it will be %s </body></html>" % (offset , dt)
	return HttpResponse(html)


	
