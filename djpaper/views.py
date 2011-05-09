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

def show_paper(request):
	error = False
	if q in request.GET and request.GET['q']:
		q = request.GET['q']
		paper = Paper.objects.filter(title__icontains=q)
		return render_to_response('show_paper.html',{'paper':paper,'query':q})
	else:
		error = True
	return render_to_response('show_paper.html',{'error':error })

def show_paper_by_id(request,paper_id):
	error = False
	paper = Paper.objects.all().get(id=paper_id)
	if paper :	
		return render_to_response('show_paper.html',{'paper':paper,})
	else:
		error = True
		return render_to_response('show_paper.html',{'error':error })


def search_paper(request,q):
	error = False
	title = ''+q
	paper = Paper.objects.filter(title__icontains = q )
	return render_to_response('show_paper.html',{'paper':paper})

def add_paper(request):
	info="Just for test"
	return render_to_response('add_paper.html',{'info':info})

	
	
