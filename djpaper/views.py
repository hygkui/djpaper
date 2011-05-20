# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from djpaper.models import Paper,Department,Pic,People

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

def show_paper_by_id(request,paper_id):
	error = False
	paper = Paper.objects.all().get(id=paper_id)
	pic = Pic.objects.all().filter(paper=paper_id) 
	if paper :	
		return render_to_response('show_paper_by_id.html',{'paper':paper,'pic':pic,})
	else:
		error = True
		return render_to_response('show_paper_by_id.html',{'error':error })


def search_paper(request,q):
	error = False
	title = ''+q
	paper = Paper.objects.filter(title__icontains = q )
	return render_to_response('show_paper.html',{'paper':paper})

def show_all_people(request):
	error = False
	people = People.objects.all()
	if people:
		return render_to_response('show_all_people.html',{'people':people})
	else:
		error = True
		return render_to_response('show_all_people',{'error':error})

def show_people_by_id(reqeuest,p_id):
	error = False
	people = People.objects.all().get(id=p_id)
	paper = Paper.objects.all().filter(author=p_id)
	if people:
		department = people.departTree
		lvl = department.level
		_departTree = ""
		while lvl:
			_departTree = department.name + ">" +  _departTree
			department = department.parent
			lvl = lvl - 1
		return render_to_response('show_people_by_id.html',{'people':people,'departTree':_departTree,'paper':paper,})
	else:
		return render_to_response('show_people_by_id.html',{'error':error})
 

