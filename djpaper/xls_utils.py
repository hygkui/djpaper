from xlrd import open_workbook,cellname
from djpaper.models import Paper,People,Department,Publication,Type,Publisher
from types import *
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
OPEN_WORKBOOK_ERROR = 'faild to open the workbook'

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


def _xls_file_save(request):
	data = get_excel_data('/home/ghh/dj/djpaper/simple.xls')
	count = 0
	for each_line in data:
		if _xls_each_line_save(each_line):
			count = count + 1
	variables=RequestContext(request,{
		'paper':'ok',
		'count':count
	})
	return render_to_response('xls_file.html',variables)

def _xls_each_line_save(each_line):
	flag_rtn = 0	
	#create or get paper
	_department,dp_dummy = Department.objects.get_or_create(name=each_line[0],level=0)
	_people,po_dummy = People.objects.get_or_create(name=each_line[1],departTree=_department)
	_classType,ct_dummy = Type.objects.get_or_create(name=each_line[6])
	_publisher,plr_dummy = Publisher.objects.get_or_create(name="unknown")
	_publication,pl_dummy = Publication.objects.get_or_create(name=each_line[3],reg=each_line[4],classType=_classType,publisher=_publisher)
			
	date=datetime.datetime.now()	
	paper,p_dummy = Paper.objects.get_or_create(
		title=each_line[2],
		publication = _publication,
		pub_date = date,
	)
	if p_dummy:
		flag_rtn = 1
	paper.author.add(_people)
	paper.save()
	return flag_rtn

