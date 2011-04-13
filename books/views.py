# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from books.models import Book

def search_form(request):
	return render_to_response('search_form.html')

##old for test,just show the search_form's result
#def search(request):
#	if 'q' in request.GET:
#		if request.GET['q']:	
#			msg = 'you searched for : %r ' % request.GET['q']
#		else:
#			msg = ' you submitted an empty form .'
#	return HttpResponse(msg)
def search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		books = Book.objects.filter(title__icontains = q )
		return render_to_response('search_result.html', { 'books':books , 'query' : q} )
	else:
#		return HttpResponse('Please submit a search form - - ')
		return render_to_response('search_form.html', {'error':True })
 
