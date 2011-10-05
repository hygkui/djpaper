from django.db.models import Q
from djpaper.models import *
from djpaper.forms import ShowDepartPerYear
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from django.views.decorators.cache import cache_page
import re

def show_statistics(request):
	papers=[]
	form = ShowDepartPerYear()
	show_result = False
	errors = []
	if request.GET.has_key('departTree') and request.GET.has_key('year'):
		departTree = request.GET['departTree'].strip()
		year = request.GET['year'].strip()
		form = ShowDepartPerYear({'departTree':departTree,'year':year})
	# is year valid?
		if re.match(r'(\d\d\d\d)',year):
			tmp_depart = Department.objects.all().filter(name__exact=departTree)
			if tmp_depart:
				people_obj = People.objects.all().filter(departTree=tmp_depart)
				if people_obj:
					for p in people_obj:
						papers += Paper.objects.all().filter(
						Q(pub_date__year=year),
						Q(first_au__exact=p.id))
					show_result = True
				else:
					errors.append('no people find in this %s',departTree)
			else:
				errors.append('department does not exist.')
		else: 
			errors.append('please input yyyy(0-9) format')
	variables = RequestContext(request,{
		'form':form,
		'papers':papers,
		'show_result':show_result,
		'count':len(papers),
		'errors':errors,
		})
	return render_to_response('depart_search.html',variables)
	
def get_statistics(depart_id,year):
	papers=[]
	# is data valid?
	if re.match(r'(\d\d\d\d)',year) and re.match(r'(\d+)',depart_id):
		people_obj = People.objects.all().filter(departTree=depart_id)
		if people_obj:
			for p in people_obj:
				papers += Paper.objects.all().filter(
				Q(pub_date__year=year),
				Q(first_au__exact=p.id))
	return papers

@cache_page(60 * 15)	
def data_maker(request):
	data_list = []
	depart = request.GET['depart']
	if re.match(r'(\d+)',depart):
		before_year = datetime.now().year-5
		now_year = datetime.now().year
		for year in range(before_year,now_year):  
		### need year+1 , or will wrong . ###
			data_list.append( {'year':year+1,'papers':get_statistics(depart,str(year)) } )
	variables = RequestContext(request,{'data_list':data_list})
	return render_to_response('show_statistics.html',variables)

def show_data_by_depart(request):
	departs = Department.objects.all().order_by	('id')
	return render_to_response('show_departs',RequestContext(request,{'departs':departs}))	
