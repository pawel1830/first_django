from django.conf.urls import url
import django.contrib.auth.views as auth_view
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name="index"),
    url(r'^login/$', auth_view.login, {'template_name': 'login.html'}, name='login'),
    url(r'^todo/add/$', views.NewTodoView.as_view(), name='todo-add' ),
    url(r'^todo/(?P<pk>[\w ]+)/delete/$', views.DeleteTodoView.as_view(), name='todo-delete'),
    url(r'^todo/(?P<pk>[\w ]+)/edit/$', views.EditTask.as_view(), name="todo-edit"),
    url(r'^todo/(?P<pk>[\w ]+)/detail/$', views.TaskDetailView.as_view(), name="todo-info"),
    url(r'^list/add/$', views.NewListView.as_view(), name='list-add' ),
    url(r'^list/add-task/(?P<title>[\w ]+)/$', views.NewTodoView.as_view(), name='list-add-task' ),
    url(r'^list/(?P<pk>[\w ]+)/delete/$', views.DeleteListView.as_view(), name='list-delete' ),
    url(r'^list/(?P<pk>[\w ]+)/edit/$', views.EditList.as_view(), name='list-edit' ),
    url(r'^logout/$', auth_view.logout, {'next_page': '/'}, name='logout'),
    url(r'^user/$', views.UserView.as_view(), name='user'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup')
#    urlpatterns(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(path.dirname(__file__), 'static')}),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
