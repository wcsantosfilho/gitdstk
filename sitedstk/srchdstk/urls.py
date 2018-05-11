from django.urls import path

from . import views

app_name = 'srchdstk'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:ling_id>/', views.detalheLing, name='detalheLing'),
    path('buscaRepos/', views.buscaRepos, name='buscaRepos'),
]