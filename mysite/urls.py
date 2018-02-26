
from django.conf.urls import url,include
from django.contrib import admin
import todos.urls
urlpatterns = [
    url(r'^', include(todos.urls)),
    url(r'^admin/', admin.site.urls),
]