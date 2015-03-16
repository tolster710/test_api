from django.forms import ModelForm
from django import forms
from models import Entry



class EntryForm(ModelForm):
	class Meta:
		model = Entry
		field = ['entry']
		exclude = ['slug']