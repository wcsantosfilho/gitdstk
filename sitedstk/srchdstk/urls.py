from django.urls import path

from . import views

app_name = 'srchdstk'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:ling_id>/', views.detalheLing, name='detalheLing'),
    path('detalheBusca/<int:busca_id>/', views.detalheBusca, name='detalheBusca'),
    path('detalheRepo/<int:repo_id>/', views.detalheRepo, name='detalheRepo'),
    path('buscaRepos/', views.buscaRepos, name='buscaRepos'),
    path('linguagem/', views.LinguagemList.as_view(), name='linguagem-list'),
    path('linguagem/<int:pk>/', views.LinguagemDetail.as_view(), name='linguagem-detail'),
    path('linguagem/add/', views.LinguagemCreate.as_view(), name='linguagem-add'),
    path('linguagem/<int:pk>/delete/', views.LinguagemDelete.as_view(), name='linguagem-delete'),
]