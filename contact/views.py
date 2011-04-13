# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

def contact(request):	
	errors = []
	if request.method == "POST":
		if not request.POST.get('subject',''):
			errors.append('Enter a subject')
		if not request.POST.get('message',''):
			errors.append('enter a message')
		if request.POST.get('email') and '@' not in request.POST['email']:
			errors.append('enter a valid email address.')
		if not errors:
#			send_mail(
#				request.POST['subject'],
#				request.POST['message'],
#				request.POST.get('email','noreply@example.com'),
#				['admin@example.com'],
#			)	
			return HttpResponseRedirect('/contact/thanks/')
	return render_to_response('contact_form.html',
			{'errors':errors,
			'subject':request.POST.get('subject',''),
			'message':request.POST.get('message',''),
			'email':request.POST.get('email',''),
			})

def thanks(request):
	return	render_to_response('thanks.html')
	
