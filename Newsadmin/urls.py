"""Newsadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
import Adminpage.views as view
import News.views as view2


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.list_learn_news),
    url(r'^list_learn_news/', view.list_learn_news, name='list_learn_news'),
    url(r'^toggle_learn_news/', view.toggle_learn_news, name='toggle_learn_news'),
    url(r'^list_real_news/', view.list_real_news, name='list_real_news'),
    url(r'^toggle_real_news/', view.toggle_real_news, name='toggle_real_news'),
    url(r'^push_real2learn/', view.push_real2learn, name='push_real2learn'),
    url(r'^statistics_news/', view.statisticsnews, name='statistics_news'),
    url(r'^receive_news/', view2.receive_news, name='receive_news'),
    url(r'^web_news/', view2.web_news, name='web_news'),
    url(r'^learn/', view2.learn, name='learn'),
    url(r'^apply_version/', view2.apply_version, name='apply_version'),
    url(r'^learn_news/', view2.learn_news, name='learn_news'),

]
