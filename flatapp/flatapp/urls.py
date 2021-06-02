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
    AboutTemplateView, FlatCreateView, FlatDeleteView, FlatUpdateView, \
    MeterCreateView, MeterTypeCreateView, MeterValueUpdateView, \
    MeterDeleteView, ProviderCreateView, ProviderTypeCreateView, \
    ProviderUpdateView, ProviderDeleteView, ProviderListView, \
    ProviderTypeUpdateView, ProviderTypeListView, ProviderTypeDeleteView

import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view,
         name='index'),
    path('flats/', FlatListView.as_view(),
         name='flats'),
    path('create/', FlatCreateView.as_view(),
         name='flat-create'),
    path('flat/<int:pk>/', FlatDetailView.as_view(),
         name='flat-details'),
    path('update/<int:pk>/', FlatUpdateView.as_view(),
         name='flat-update'),
    path('delete/<int:pk>/', FlatDeleteView.as_view(),
         name='flat-delete'),
    path('meter/create/', MeterCreateView.as_view(),
         name='meter-create'),
    path('meter/create/<int:pk>/', MeterCreateView.as_view(),
         name='meter-create'),
    path('meter/delete/<int:pk>/', MeterDeleteView.as_view(),
         name='meter-delete'),
    path('metertype/create/', MeterTypeCreateView.as_view(),
         name='metertype-create'),
    path('provider/create/', ProviderCreateView.as_view(),
         name='provider-create'),
    path('provider/<int:pk>/', ProviderUpdateView.as_view(),
         name='provider-update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(),
         name='provider-delete'),
    path('providers/', ProviderListView.as_view(),
         name='providers'),
    path('providertype/create/', ProviderTypeCreateView.as_view(),
         name='providertype-create'),
    path('providertype/<int:pk>/', ProviderTypeUpdateView.as_view(),
         name='providertype-update'),
    path('providertype/delete/<int:pk>/', ProviderTypeDeleteView.as_view(),
         name='providertype-delete'),
    path('providertypes/', ProviderTypeListView.as_view(),
         name='providertypes'),
    path('metervalue/update/<int:pk>/', MeterValueUpdateView.as_view(),
         name='metervalue-update'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('__debug__/', include(debug_toolbar.urls)),
]
