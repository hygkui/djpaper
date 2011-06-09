# Create your views here.
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from djpaper.models import Paper,Department,Pic,People,Commit,CommitForm,ShortMessage,SMForm,Tag
#from djpaper.forms import CommitForm

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
	commit = Commit.objects.all().filter(paper=paper_id)
	form = CommitForm()
	if request.method == 'POST':
		data = request.POST.copy()#else u cannot change the value of the data
		data['paper'] = paper_id
		form = CommitForm(data)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('')
	if paper :	
		return render_to_response('show_paper_by_id.html',{'paper':paper,'pic':pic,'commit':commit,'form':form,},RequestContext(request))
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

def show_people_by_id(request,p_id):
	error = False
	people = People.objects.all().get(id=p_id)
	paper = Paper.objects.all().filter(author=p_id)
	short_msg = ShortMessage.objects.all().filter(dest=p_id)
	form = SMForm()	
	if request.method == "POST":
		data = request.POST.copy()
		data['dest'] = p_id
		data['isRead']=False
		form = SMForm(data)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('')
	if people:
		department = people.departTree
		lvl = department.level
		_departTree = ""
		while lvl:
			_departTree = department.name + ">" +  _departTree
			department = department.parent
			lvl = lvl - 1
		return render_to_response('show_people_by_id.html',{'people':people,'departTree':_departTree,'paper':paper,'short_msg':short_msg,'form':form},RequestContext(request))
	else:
		return render_to_response('show_people_by_id.html',{'error':error})


def tag_cloud_page(request):
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
	vars = RequestContext( request , {
		'tags':tags
	})
	return render_to_response('tag_cloud_page.html',vars)

