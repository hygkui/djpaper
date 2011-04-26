# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from djpaper.models import Paper,Department

def show_all_papers(request):
	error = False
	papers = Paper.objects.all()
	if papers:
		return render_to_response('show_all_papers.html',{'papers':papers } )
	else:
		error = True
		return render_to_response('show_all_papers.html',{'error':error})

def show_departments(request):
	error = False
	departments = Department.objects.all()
	print_ = []
	if departments:
		for dep in departments:
			print_.append( print_deps(dep) )
		return render_to_response('show_departments.html',{'departments':departments,'print_':print_ } )
	else:
		error = True
		return render_to_response('show_departments.html',{'error':error})


def print_deps(dep):
		if dep.parent:
			return	print_deps(dep.parent)+ '' +dep.name
		else: 
			return dep.name


	
