# Create your views here.
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from djpaper.models import Paper,Department,Pic,People,Commit,ShortMessage,SMForm,Tag,RegistrationForm,PaperForm,PicForm
from django.views.decorators.cache import cache_page
from djpaper.forms import SearchForm
from django.db.models import Q
from djpaper.paginator_utils import paginator_maker
from django.contrib.auth.decorators import login_required
from datetime import datetime

##@cache_page( 60 * 15 ) 
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
	if request.GET.has_key('page'):
		page = request.GET.get('page')
	else:
		page = 1
	papers = paginator_maker(query_set,page)
	variables = RequestContext(request,{
		'papers':papers,
		'count':count,
	})
	return render_to_response('show_all_papers.html',variables)

##@cache_page( 60 * 15 )
def show_departments(request):
	error = False
	departments = Department.objects.all()
	print_ = []
	if departments:
		return render_to_response('show_departments.html',{'departments':departments}  ,RequestContext(request))
	else:
		error = True
		return render_to_response('show_departments.html',{'error':error})


def print_deps(dep):
		if dep.parent:
			return	print_deps(dep.parent)+ '' +dep.name
		else: 
			return dep.name

##@cache_page( 60 * 15 )
def show_paper_by_id(request,paper_id):
	error = False
	paper = Paper()
	try:
		paper = Paper.objects.all().get(id=paper_id)
	except paper.DoesNotExist:
		error = True
	pic = Pic.objects.all().filter(paper=paper_id)
	variables = RequestContext(request,	{'paper':paper,'pic':pic,'error':error})
	return render_to_response('show_paper_by_id.html',variables)



##@cache_page( 60 * 15 )
def show_all_people(request):
	count = 0
	show_all = True
	if request.GET.has_key('name'):
		query_set = People.objects.filter(name__icontains=request.GET['name'].strip()).order_by('-id')
		show_all = False
	else:
		query_set = People.objects.all().order_by('-id')

	count = query_set.count()
	if request.GET.has_key('page'):
		page = request.GET.get('page')
	else:
		page = 1
	people = paginator_maker(query_set,page)
	variables = RequestContext(request,{
		'people':people,
		'show_all':show_all,
		'count':count
	})
	return render_to_response('show_all_people.html',variables)

##@cache_page( 60 * 15 )
def show_people_by_id(request,p_id):
	error = False
	people = People.objects.all().get(id=p_id)
	paper = Paper.objects.all().filter(first_au=p_id).order_by('-id')
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
	form = RegistrationForm()
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1'],
				email = form.cleaned_data['email']
			)
			return HttpResponseRedirect('/register/errors/')
	
	variables = RequestContext(request, { 'form':form} )
	return render_to_response('registration/register.html',variables)

def search_paper(request):
	form = SearchForm()
	papers = []
	show_results = False
	query=''
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
			count =query_set.count()
			if request.GET.has_key('page'):
				page = request.GET.get('page')
			else:
				page = 1
			papers = paginator_maker(query_set,page)
	variables = RequestContext(request,{'form':form,
			'papers':papers,
			'count':count,
			'query':query,
			'show_tags':True,
			'show_results':show_results,
            'show_user':True,
		})
	if request.GET.has_key('ajax'):
		return render_to_response('paper_list.html',variables)
	else:
		return render_to_response('search.html',variables)

##@cache_page( 60 * 15 )
def show_paper_by_tag(request,tag_title):
	tag = Tag.objects.all().get(title=tag_title)
	papers = tag.paper_set.all()
	show_results = False
	count = 0
	if  papers.count() :
		show_results = True	
		count = papers.count()
		if request.GET.has_key('page'):
			page = request.GET.get('page')
		else:
			page = 1
		papers = paginator_maker(papers,page)
	variables = RequestContext(request,{'papers':papers,
			'count':count,
			'show_tags':True,
			'show_results':show_results,
			'show_user':True,
		})
	return render_to_response('paper_list.html',variables)

### tag-add
def tag_add(request,p_id):
	succ = False
	paper = Paper.objects.get(id=p_id)
	if request.method == 'POST':
		title=request.POST['title'].strip()
		if title:
			tag = Tag.objects.all().filter(title=title)
			if tag:
				tag = tag.get(title=title)
			else:
				tag = Tag(title=title)
				tag.save()
			try:
				tag.paper_set.add(paper)
			except:
				pass
	return show_paper_by_id(request,p_id)

def paper_edit(request,p_id):
	paper = Paper.objects.get(id=p_id)
	flag = 0 # 0 stands for show , 1 stands for write to the db.
	if request.method == 'POST':
		flag = 1
		form = PaperForm(request.POST,instance=paper)
		form.save()
	else: 
		form = PaperForm(instance=paper)
	variables = RequestContext(request,{'form':form,'p_id':p_id})
	if flag:
		return	show_paper_by_id(request,p_id) 
	else:
		return render_to_response('paper_edit.html',variables)

@login_required()
def pic_upload(request,p_id):
	succ = False
	paper = Paper.objects.get(id=p_id)
	if 'file' in  request.FILES:
		image = request.FILES['file']
		s = Pic(upload_date=datetime.now(),paper=paper,image=image)
		s.save()
		succ = True
	form = PicForm(request.POST)
	variables = RequestContext(request,{'form':form,'p_id':p_id,'succ':succ})
	if not succ:
		return render_to_response('pic_upload.html',variables)		
	else:
		return show_paper_by_id(request,p_id)
	
@login_required()
def abs_edit(request,p_id):
	succ = False
	paper = Paper.objects.get(id=p_id)
	if request.POST.has_key('content'):
		content = request.POST['content'].strip()
		if content:
			paper.abstract = content
			paper.save()
			succ = True
	return show_paper_by_id(request,p_id)
		
############################################
## author can add only if he/she exists. ###
############################################
@login_required()
def author_add(request,p_id):
	paper = Paper.objects.get(id=p_id)
	authors = paper.other_au.all()
	if request.POST.has_key('author') and request.POST.has_key('depart'):
		author = request.POST['author'].strip()
		depart = request.POST['depart'].strip()
		try:
			au = People.objects.get(name=author,departTree=Department.objects.get(name=depart))
		except:
			pass
		if au:
			au.paper_set.add(paper)
	return show_paper_by_id(request,p_id)
				
