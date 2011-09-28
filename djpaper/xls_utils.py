import os
from xlrd import open_workbook,cellname
from djpaper.models import Paper,People,Department,Publication,Type,Publisher
from types import *
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
OPEN_WORKBOOK_ERROR = 'faild to open the workbook'
from djpaper.forms import XlsSaveForm,SearchFormName,SearchFormDepartTree
from django.db.models import Q
import settings

def get_excel_data(xls_file):
	# need to check if xls_file is a filename 
	# and get from the request or a filebox by the django form elements.
	try:
		book = open_workbook(xls_file)
	except:
		return OPEN_WORKBOOK_ERROR
	sheet = book.sheet_by_index(0)
	orig_data=[]
	for row_index in range(1,sheet.nrows):
		temp =[]
   		for col_index in range(sheet.ncols):
			temp.append(sheet.cell(row_index,col_index).value)
		orig_data.append(temp)
	return orig_data	

def _xls_each_line_save(each_line):
#	flag_rtn = 0	
	#create or get paper
	_department,dp_dummy = Department.objects.get_or_create(name=each_line[0],level=0)
	_people,po_dummy = People.objects.get_or_create(name=each_line[1],departTree=_department)
	_classType,ct_dummy = Type.objects.get_or_create(name=each_line[6])
	#warning!!!
	_publisher,plr_dummy = Publisher.objects.get_or_create(name="unknown")
	_publication,pl_dummy = Publication.objects.get_or_create(name=each_line[3],reg=each_line[4],classType=_classType,publisher=_publisher)
	
	if '.' in str(each_line[5]):
		dt_split=str(each_line[5]).split('.')
	else: 
		#warning!!!
		dt_split=['1111','11']
	if len(dt_split[1])==1:
		dt_split[1]='0'+dt_split[1]
	pub_date_str = dt_split[0] + dt_split[1]	
	
	if _people:
		paper,p_dummy = Paper.objects.get_or_create(
			title=each_line[2],
			first_au = _people,
			publication = _publication,
			pub_date = datetime.datetime.strptime(str(pub_date_str),'%Y%m'),
		)
	else:
		paper,p_dummy = Paper.objects.get_or_create(
			title=each_line[2],
			first_au = po_dummy,
			publication = _publication,
			pub_date = datetime.datetime.strptime(str(pub_date_str),'%Y%m'),
		)
#	if p_dummy:
#		flag_rtn = 1
	paper.other_au = []	
	paper.save()
	if p_dummy:
		return paper.id
	else:
		return 0

def _xls_file_save(request):
	show_results = False
	papers=[]
	if request.method == 'POST':
		form = XlsSaveForm(request.POST,request.FILES)
		if form.is_valid():
			show_results = True
			data = get_excel_data(request.FILES['file'].temporary_file_path())
			for each_line in data:
				new =_xls_each_line_save(each_line)
				if new:
					papers.append( Paper.objects.get(id=new) )
	else:
		form = XlsSaveForm()
	variables=RequestContext(request,{
		'form':form,
		'count':len(papers),
		'papers':papers,
		'show_results':show_results
	})
	return render_to_response('xls_file_save.html',variables)

def _xls_file_out_page(request):
	show_result_departTree = False
	show_result_name = False
	form_departTree = SearchFormDepartTree()
	form_name = SearchFormName()
	papers =[]
	peoples = []
	if request.GET.has_key('departTree'):
		show_result_departTree = True
		query = request.GET['departTree'].strip()
		form_departTree = SearchFormDepartTree({'departTree':query})
		if query:
			keywords = query.split()
			q = Q()
			for keyword in keywords:
				q = q | Q(name__icontains=keyword)
			depart_obj = Department.objects.filter(q).order_by('id')
			for depart in depart_obj:
				for people in depart.people_set.all():
					peoples.append(people)
	elif request.GET.has_key('name'):
		show_result_name = True
		query = request.GET['name'].strip()
		form_name = SearchFormName({'name':query})
		if query:
			keywords = query.split()
			q = Q()
			for keyword in keywords:
				q = q | Q(name__icontains=keyword)
			peoples = People.objects.filter(q).order_by('id')
	variables=RequestContext(request,{
		'peoples':peoples,
		'show_result_departTree':show_result_departTree,
		'show_result_name':show_result_name,
		'form_name':form_name,
		'form_departTree':form_departTree,
		'count':len(peoples)
	})
	return render_to_response('xls_file_out.html',variables)

