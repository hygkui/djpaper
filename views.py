from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout
from django.template import RequestContext
from djpaper.models import Paper,Tag
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

def tag_cloud_cal():
	MAX_WEIGHT = 5
	tags = Tag.objects.order_by('title')
	min_count = max_count = tags[0].paper_set.count() 
	for tag in tags:
		tag.count = tag.paper_set.count()
		if tag.count < min_count:
			min_count = tag.count
		if tag.count > max_count:
			max_count = tag.count
	# calculate count range ,avoid dividing by zero.	
	range = float( max_count - min_count )
	if range == 0.0:
		range = 1.0
	#calculate tag weight
	for tag in tags:
		tag.weight = int(
			MAX_WEIGHT * (tag.count - min_count ) / range
		)
	return tags

def top_10():
	return Paper.objects.all()[:10]	


def index(request):
	tags = tag_cloud_cal()
	papers = top_10()
	variables = RequestContext( request, {'papers':papers,'tags':tags} )
	return render_to_response('index.html',variables)


def about(request):
	info = ''
	return render_to_response('about.html',{'info':info},RequestContext(request))	

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')
