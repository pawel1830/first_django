from django import forms
from models import Tasks, User, Lists
from django.contrib.auth.forms import UserCreationForm
import logging

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('title', 'details', 'list_id', 'image')

    def save(self, user=None):
        task_form = super(TaskForm, self).save(commit=False)
        if user:
            task_form.owner_id = user
        task_form.save()
        return task_form

    def __init__(self, user, list_title=None, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['list_id'] = forms.ModelChoiceField(queryset=Lists.objects.filter(owner=user), to_field_name="title",
                                                        empty_label=None)
        self.fields['list_id'].label = "Your list"
        if list_title:
            self.fields['list_id'].widget = forms.HiddenInput()
            self.fields['list_id'].initial = list_title


class ListForm(forms.ModelForm):
    class Meta:
        model = Lists
        fields = ('title', 'details')

    def save(self, user=None):
        list_form = super(ListForm, self).save(commit=False)
        if user:
            list_form.owner_id = user
        list_form.save()
        return list_form


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username','email',  'first_name', 'last_name', 'password1', 'password2', )