# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    New User extend default django User model,
    set username as primary key and set first name, last name and email to required
    """
    username = models.CharField(primary_key=True, max_length=50, unique=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        db_table = 'Users'

class Lists(models.Model):
    """
    This class represents table with list of tasks
    """
    title = models.CharField(max_length=128)
    details = models.TextField(null=True)
    owner = models.ForeignKey(User, to_field='username', related_name='lists_r', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Lists'
    def __str__(self):
        return self.title
class Tasks(models.Model):
    """
    This class represent Tasks table in django model
    """
    title = models.CharField(max_length=128)
    details = models.TextField(null=True)
    image = models.ImageField(blank=True, null=True, upload_to="image")
    created_date = models.DateTimeField(auto_now_add=True)
    task_end = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True)
    owner = models.ForeignKey(User, to_field='username', related_name='user_tasks_r', on_delete=models.CASCADE)
    list_id = models.ForeignKey(Lists,related_name='list_task_r')

    class Meta:
        db_table = 'Tasks'

    def __repr__(self):
        return "title=%s details=%s" % (self.title, self.details)