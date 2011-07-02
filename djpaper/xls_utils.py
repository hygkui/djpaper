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


### for test
###data =  get_excel_data('simple.xls')
###if type(data) is ListType:
###	for dd in data:
###		for xx in dd:	
###			print xx
###		print '---------'
###else:
###	print data 
###	




###
# the xls file must be format very strict 
# in order to clean the data quickly and clearly and accurately.
def clean_data(data):
	if type(data) is ListType:
		department=[]
 		author=[]
 		title=[]
 		public_name=[]
 		public_isbn=[]
 		pub_date=[]
 		paper_type=[]
		for each_line in data:
			department.append(each_line[0])
			author.append( each_line[1])
			title.append( each_line[2])
			public_name.append( each_line[3])
			public_isbn.append(each_line[4])
			pub_date.append( each_line[5])
			paper_type.append( each_line[6])
		for dep in author:		
			print dep
	else:
		print data
	cl_data=[ department, author, title, public_name, public_isbn, pub_date, paper_type]
	return cl_data
	
#zz = clean_data( get_excel_data('simple.xls'))	
##print zz.department


def _xls_file_save(request):
	data = get_excel_data('/home/ghh/dj/djpaper/simple.xls')
	papers=[]
	for each_line in data[:50]:
		#create or get paper
		_classType,ct_dummy = Type.objects.get_or_create(name=each_line[6])
		_department,dp_dummy = Department.objects.get_or_create(name=each_line[0],level=0)
		_people,po_dummy = People.objects.get_or_create(name=each_line[1],departTree=_department)
		_publisher,plr_dummy = Publisher.objects.get_or_create(name="unknown")
		_publication,pl_dummy = Publication.objects.get_or_create(name=each_line[3],reg=each_line[4],classType=_classType,publisher=_publisher)
		date=datetime.datetime.now()	
		paper = Paper.objects.create(
			title=each_line[2],
			publication = _publication,
			pub_date = date,
		)
		papers.append(paper)
		#paper.people_set.add(_people)
		#paper.save()
	variables=RequestContext(request,{
		'papers':papers,
	})
	return render_to_response('xls_file.html',variables)
