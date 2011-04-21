# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from contact.forms import ContactForm

def contact(request):	
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			return HttpResponseRedirect('/contact/thanks/')
	else:
		form = ContactForm()
	return render_to_response('contact_form.html',{'form': form })

def thanks(request):
	return	render_to_response('thanks.html')
	
