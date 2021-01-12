from django import forms
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import PasswordChangeForm

from .models import *


class AddTodoForm(forms.ModelForm):
	class Meta:
		model = ToDoTask
		fields = ('task', )

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['task'].widget.attrs.update({'class': 'form-control', 'rows': '8'})


class PasswordChangeFormEdit(FormMixin, PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['old_password'].widget.attrs.update({'class' : 'form-control'})
		self.fields['new_password1'].widget.attrs.update({'class' : 'form-control'})
		self.fields['new_password2'].widget.attrs.update({'class' : 'form-control'})


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', )

	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['readonly'] = True
		self.fields['email'].widget.attrs['readonly'] = True
		self.fields['username'].widget.attrs.update({'class' : 'form-control'})
		self.fields['email'].widget.attrs.update({'class' : 'form-control'})
		self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
		self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})


class ProfileDetailForm(forms.ModelForm):
	class Meta:
		model = RegisteredUser
		fields = ('date_of_birth', )

	def __init__(self, *args, **kwargs):
		super(ProfileDetailForm, self).__init__(*args, **kwargs)
		self.fields['date_of_birth'].widget.attrs.update({'class' : 'form-control'})
