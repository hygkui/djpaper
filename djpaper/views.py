# Create your views here.
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from djpaper.models import Paper,Department,Pic,People,Commit,CommitForm,ShortMessage,SMForm,Tag,RegistrationForm
from django.views.decorators.cache import cache_page
from djpaper.forms import SearchForm
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
ITEMS_PER_PAGE = 15


def show_all_papers(request):
	count = 0
	show_all = True
	papers=[]
	if request.GET.has_key('title'):
		query_set = Paper.objects.filter(title__icontains=request.GET['title'].strip()).order_by('-id')
		show_all = False
	else:
		query_set = Paper.objects.all().order_by('-id')

	count = query_set.count()
	paginator = Paginator(query_set,ITEMS_PER_PAGE)
	if request.GET.has_key('page'):
		page = request.GET.get('page')
	else:
		page = 1
	try:
		papers = paginator.page(page)
	except PageNotAnInteger:
		papers = paginator.page(1)
	except EmptyPage:
		papers = paginator.page(paginator.num_pages)
	variables = RequestContext(request,{
		'papers':papers,
		'count':count,
	})
	return render_to_response('show_all_papers.html',variables)

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
	count = 0
	show_all = True
	if request.GET.has_key('name'):
		query_set = People.objects.filter(name__icontains=request.GET['name'].strip()).order_by('-id')
		show_all = False
	else:
		query_set = People.objects.all().order_by('-id')

	count = query_set.count()
	paginator = Paginator(query_set,ITEMS_PER_PAGE)
	if request.GET.has_key('page'):
		page = request.GET.get('page')
	else:
		page = 1
	try:
		people = paginator.page(page)
	except PageNotAnInteger:
		people = paginator.page(1)
	except EmptyPage:
		people = paginator.page(paginator.num_pages)
	variables = RequestContext(request,{
		'people':people,
		'show_all':show_all,
		'count':count
	})
	return render_to_response('show_all_people.html',variables)

@cache_page( 60 * 15 )
def show_people_by_id(request,p_id):
	error = False
	people = People.objects.all().get(id=p_id)
	paper = Paper.objects.all().filter(author=p_id).order_by('-id')
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
	count = 0
	if request.GET.has_key('query'):
		show_results = True
		query = request.GET['query'].strip()
		if query:
			keywords = query.split()	
			q = Q()
			for keyword in keywords:
				q = q & Q(title__icontains=keyword)
			form = SearchForm( {'query' : query })
			query_set = Paper.objects.filter(q).order_by('-id')
			paginator = Paginator(query_set,ITEMS_PER_PAGE)
			count = paginator.count
			if request.GET.has_key('page'):
				page = request.GET.get('page')
			else:
				page = 1
			try:
				papers = paginator.page(page)
			except PageNotAnInteger:
				papers = paginator.page(1)
			except EmptyPage:
				papers = paginator.page(paginator.num_pages)
		
	variables = RequestContext(request,{'form':form,
			'papers':papers,
			'count':count,
			'show_tags':True,
			'show_results':show_results,
            'show_user':True,
		})
	if request.GET.has_key('ajax'):
		return render_to_response('paper_list.html',variables)
	else:
		return render_to_response('search.html',variables)

