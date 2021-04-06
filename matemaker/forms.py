from django import forms
from matemaker.models import UserProfile, Genre,Interest, Post
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
		exclude = ('genre','date','creator','slug')

class PostForm(forms.ModelForm):
    message = forms.CharField(max_length=128,
                            help_text="Message @everyone")

    class Meta:
        model = Post
        fields = ('message',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )	
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture','website')
