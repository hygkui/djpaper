from django.http import HttpResponse
from djpaper.models import Paper,People
from django.views.decorators.cache import cache_page
def ajax_title_autocomplete(request):
	if request.GET.has_key('q'):
		papers = Paper.objects.filter(title__istartwith=request['q'])[:10]
		return HttpResponse('\n'.join(paper.title for paper in papers))
	return HttpResponse()

@cache_page( 60*15 )
def ajax_people_autocomplete(request):
	if request.GET.has_key('q'):
		query = request.GET['q'].strip()
		peoples = People.objects.filter(name__contains=query)[:10]
		return HttpResponse('\n'.join(people.name for people in peoples))
	return HttpResponse()
	
