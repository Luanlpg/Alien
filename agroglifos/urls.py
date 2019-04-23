from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='cadastro'),
    path('register_occur/', views.register_occur, name='registrar_correncia'),
    path('list_occurrences/', views.list_occurrences, name='listar_ocorrencias'),
    path('summary/', views.summary, name='sumario'),
    path('home/', views.index2, name='home'),
    path('details/<str:uuid>/', views.details, name='details'),
]
