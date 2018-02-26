# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Tasks, Lists, User
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic.edit import DeleteView, UpdateView
from forms import TaskForm, ListForm
from django.http import HttpResponse
import json
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
import logging
from forms import SignUpForm
from django.contrib.auth.forms import PasswordChangeForm

from django.template import RequestContext
# Get an instance of a logger
logger = logging.getLogger(__name__)
class HomePageView(TemplateView):

    template_name = "dashboard.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(HomePageView, self).dispatch(request, *args, **kwargs)



class NewTodoView(FormView):
    template_name = "Tasks.html"
    form_class = TaskForm

    def form_valid(self, form):
        form.save(self.request.user)
        return super(NewTodoView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse("index")

    def get_form_kwargs(self):
        kwargs = super(NewTodoView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        if "title" in self.kwargs:
            kwargs.update({'list_title': self.kwargs['title']})
        return kwargs

class NewListView(FormView):
    template_name = "Lists.html"
    form_class = ListForm

    def form_valid(self, form):
        form.save(self.request.user)
        return super(NewListView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse("index")

class DeleteTodoView(DeleteView):
    model = Tasks
    template_name = "tasks_confirm_delete.html"
    success_url = reverse_lazy('index')
    def get_object(self, *args, **kwargs):
        task_del = get_object_or_404(Tasks, id=self.kwargs['pk'])

        return task_del

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        resp = super(DeleteTodoView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        else:
            # POST request (not ajax) will do a redirect to success_url
            return resp

class DeleteListView(DeleteView):
    model = Lists
    template_name = "tasks_confirm_delete.html"
    success_url = reverse_lazy('index')
    def get_object(self, *args, **kwargs):
        list_del = get_object_or_404(Lists, id=self.kwargs['pk'])
        return list_del

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        resp = super(DeleteListView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        else:
            # POST request (not ajax) will do a redirect to success_url
            return resp

class EditTask(UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = "Task_edit.html"

    def get_object(self, *args, **kwargs):
        todos = get_object_or_404(Tasks, id=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return todos
    def get_form_kwargs(self):
        kwargs = super(EditTask, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs
    def get_success_url(self, *args, **kwargs):
        return reverse("index")

class EditList(UpdateView):
    model = Lists
    form_class = ListForm
    template_name = "List_edit.html"

    def get_object(self, *args, **kwargs):
        lists = get_object_or_404(Lists, id=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return lists
    def get_success_url(self, *args, **kwargs):
        return reverse("index")


class TaskDetailView(DetailView):
    model = Tasks
    template_name = 'task_detail.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Tasks, id=self.kwargs['pk'])

class UserView(TemplateView):
    template_name = 'user_detail.html'

class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'