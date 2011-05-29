import datetime
from django import forms
from django.forms.util import ErrorDict
from models import Commit

#class CommitForm(forms.Form):
#	people = forms.CharField(initial="1")
#	content = forms.CharField(widget=forms.Textarea,max_length=300)
#
#	time = forms.CharField(widget=forms.HiddenInput)
#	paper = forms.IntegerField(widget=forms.HiddenInput)
#		
##	def __init__(self,target_obj_of_people,target_obj_for_paper,data=None,initial=None):
##		self.target_obj_of_people = target_obj_of_people
##		self.target_obj_for_paper = target_obj_for_paper
#	def __init__(self,data=None,initial=None):
#		if initial is None:
#			initial = { }
#		super(CommitForm,self).__init__(data=data,initial=initial)
#	
#	def get_commit_object(self):
#		if not self.valid():
#			raise ValueError('get_commit_object may only be called on valid form')
#		
#		new = Commit(
#			time = datetime.datetime.now(),
#			content = self.clean_content(),
#			people = People.objects().get(id=self.clean_data['people']),
#			paper = Paper.objects().get(id=self.clean_data['paper']),
#		)
#		return new
#		
#	def security_errors(self):
#		errors = ErrorDict()
#		return errors
# 
#	def clean_content(self):
#		content = self.clean_data['content']
#		num_words = len( content.join( content.split() ))
#		if num_words < 4:
#			raise forms.validationError('not enough words!')
#		content = content.replace('<script','&lt;script').replace('</script>','$lt;/script&gt;')
#		return content
