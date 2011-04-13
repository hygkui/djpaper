# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from books.models import Book

def search(request):
	error = False
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			error = True
		else:
			books = Book.objects.filter(title__icontains = q )
			return render_to_response('search_result.html', { 'books':books , 'query' : q} )

	return render_to_response('search_form.html', {'error': error })
 
