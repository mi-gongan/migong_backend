from django.urls import path
from . import views

urlpatterns = [
    path("analyze/", views.Analyze.as_view(), name='analyze'),
]
