from django import forms

class SearchForm(forms.Form):
	query = forms.CharField(
		label = 'Enter a keyword to search for paper',
		widget = forms.TextInput(attrs={'size':32})
	)




