from django.urls import path

from . import views

app_name = 'srchdstk'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:ling_id>/', views.detalheLing, name='detalheLing'),
    path('detalheBusca/<int:busca_id>/', views.detalheBusca, name='detalheBusca'),
    path('detalheRepo/<int:repo_id>/', views.detalheRepo, name='detalheRepo'),
    path('buscaRepos/', views.buscaRepos, name='buscaRepos'),
]