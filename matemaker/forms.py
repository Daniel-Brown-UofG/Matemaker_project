from django import forms
from matemaker.models import UserProfile, Genre,Interest
from django.contrib.auth.models import User


class GenreForm(forms.ModelForm):
	name = forms.CharField(max_length=64,
                           help_text="Please enter the genre name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	members = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Genre
		fields = ('name',)

class InterestForm(forms.ModelForm):
	name = forms.CharField(max_length=64,
                            help_text="Please enter the interest name.")
	description = forms.CharField(max_length=128,
                            help_text="Please briefly decribe the interest.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	members = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Interest
		exclude = ('genre','date','creator')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)