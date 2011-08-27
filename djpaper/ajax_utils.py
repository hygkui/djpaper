from django.http import HttpResponse
from djpaper.models import Paper

def ajax_title_autocomplete(request):
	if request.GET.has_key('q'):
		papers = Paper.objects.filter(title__istartwith=request['q'])[:10]
		return HttpResponse('\n'.join(paper.title for paper in papers))
	return HttpResponse()
