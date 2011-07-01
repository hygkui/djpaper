# Create your views here.
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from djpaper.models import Paper,Department,Pic,People,Commit,CommitForm,ShortMessage,SMForm,Tag,RegistrationForm
from django.views.decorators.cache import cache_page
from djpaper.forms import SearchForm
def show_all_papers(request):
	error = False
	papers = Paper.objects.all()
	if papers:
		return render_to_response('show_all_papers.html',{'papers':papers } ,RequestContext(request))
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
		return render_to_response('show_departments.html',{'departments':departments,'print_':print_ }  ,RequestContext(request))
	else:
		error = True
		return render_to_response('show_departments.html',{'error':error})


def print_deps(dep):
		if dep.parent:
			return	print_deps(dep.parent)+ '' +dep.name
		else: 
			return dep.name

@cache_page( 60 * 15 )
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




def show_all_people(request):
	error = False
	people = People.objects.all()
	if people:
		return render_to_response('show_all_people.html',{'people':people} ,RequestContext(request))
	else:
		error = True
		return render_to_response('show_all_people',{'error':error})

@cache_page( 60 * 15 )
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

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1'],
				email = form.cleaned_data['email']
			)
			return HttpResponseRedirect('/register/success/')
	else :
		form = RegistrationForm()
	variables = RequestContext(request, { 'form':form} )

	return render_to_response('registration/register.html',variables)

def search_paper(request):
	form = SearchForm()
	papers = []
	show_results = False
	if request.GET.has_key('query'):
		show_results = True
		query = request.GET['query'].strip()
		result_summary=""
		if query:
			form = SearchForm( {'query' : query })
			papers = Paper.objects.filter(title__icontains=query)
	variables = RequestContext(request,{'form':form,
			'papers':papers,
			'show_tags':True,
			'show_results':show_results,
			'show_user':True,
			'result_summary':result_summary
		})
	#RequestContext(request,{  })
	if request.GET.has_key('ajax'):
		return render_to_response('paper_list.html',variables)
	else:
		return render_to_response('search.html',variables)

