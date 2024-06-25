from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"), # views.AllToDos.as_view(), name="index"),
    path('experiment/run/<str:id>', views.runExperiment, name="run"),
    path('experiment/status/<str:id>', views.statusExperiment, name="status"),
    path('experiment/stop/<str:id>', views.stopExperiment, name="stop"),
    path('experiment/delete/<str:id>', views.deleteExperiment, name="delete"),
]
