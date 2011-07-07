from django import forms

class SearchForm(forms.Form):
	query = forms.CharField(
		label = 'Enter a keyword to search for paper',
		widget = forms.TextInput(attrs={'size':32})
	)
class SearchFormDepartTree(forms.Form):
	departTree = forms.CharField(
		label = 'select the depart you want ',
		widget = forms.TextInput(attrs={'size':32})
	)
class SearchFormName(forms.Form):
	name = forms.CharField(
		label = 'Enter names want ,split by space',
		widget = forms.TextInput(attrs={'size':32})
	)
	

class XlsSaveForm(forms.Form):
	file = forms.FileField()

