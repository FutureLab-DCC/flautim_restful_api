from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"), # views.AllToDos.as_view(), name="index"),
    path('experiment/run/', views.runExperiment, name="run"),
    path('experiment/status/', views.statusExperiment, name="status"),
    path('experiment/stop/', views.stopExperiment, name="stop"),
    path('experiment/delete/', views.deleteExperiment, name="delete"),
]
