"""flatapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

from flats.views import index_view, FlatListView, FlatDetailView, \
    AboutTemplateView, FlatCreateView, FlatDeleteView, FlatUpdateView
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view),
    path('flats/', FlatListView.as_view()),
    path('create/', FlatCreateView.as_view()),
    path('flat/<int:pk>/', FlatDetailView.as_view()),
    path('update/<int:pk>/', FlatUpdateView.as_view()),
    path('delete/<int:pk>/', FlatDeleteView.as_view()),
    path('about/', AboutTemplateView.as_view()),
    path('__debug__/', include(debug_toolbar.urls)),
]
