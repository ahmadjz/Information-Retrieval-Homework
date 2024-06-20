from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Adjust regex to match both .doc and .docx files correctly
    re_path(r'^doc/(?P<pk>[A-Za-z0-9_]+\.(?:docx?))/$', views.read, name='read'),

    # Redirect for favicon.ico
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
]
