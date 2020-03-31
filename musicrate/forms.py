from django import forms
from .models import *
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('album', 'rating', 'comment',)
        widgets = {
        	'comment': forms.Textarea(attrs={'rows':4, 'cols':35}),
        }

class AlbumSearchForm(forms.ModelForm):
	name = forms.CharField(required=False)
	artist = forms.CharField(required=False)
	class Meta:
		model = Album
		fields = ('name', 'artist')

class ProfileSearchForm(forms.ModelForm):
	username = forms.CharField(required=False)
	class Meta:
		model = Profile
		fields = ()

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		help_texts = {
			'username': None,
		}
		fields = ('first_name', 'last_name', 'username', 'email', 'password')
		widgets = {
			'password': forms.PasswordInput(),
		}