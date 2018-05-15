from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Max, Count, F
from django.contrib import messages
from django.views import generic

from .forms import LinguagemForm
from .models import Linguagem, Busca, Repositorio

def index(request):
    # lista buscas feitas com aquela linguagem (JOIN)
    try:
        lista_buscas = Busca.objects.annotate(max_date=Max('linguagem__busca__data_busca')).filter(data_busca=F('max_date'))
        lista_repos = Repositorio.objects.filter(busca__id__in=lista_buscas)
        print(lista_buscas, "\n")
    except IndexError:
        lista_buscas = null
        lista_repos = null
    # define contexto para passar para o template
    context = {
        'lista_repos': lista_repos
    }
    # render (request, template, query das linguagens)
    return render(request, 'srchdstk/index.html', context)


def detalheLing(request, ling_id):
    # monta lista das linguagens e suas buscas
    lista_linguagem_busca = list(Busca.objects.filter(linguagem_id=ling_id))
    # traz detalhes do Linguagem
    lingObj = Linguagem.objects.get(pk=ling_id)
    
    # Monta contexto para passar para o template
    context = {
        'linguagem': lingObj,
        'lista_linguagem_busca': lista_linguagem_busca
    }

    # Retorna o resultado no template
    return render(request, 'srchdstk/detalheLing.html', context)

def detalheBusca(request, busca_id):
    # monta lista dos repositorios da busca
    lista_repositorios_busca = list(Repositorio.objects.filter(busca_id=busca_id))
    # traz detalhes da busca
    buscaObj = Busca.objects.get(pk=busca_id)
    
    # Monta contexto para passar para o template
    context = {
        'busca': buscaObj,
        'lista_repositorios_busca': lista_repositorios_busca
    }

    # Retorna o resultado no template
    return render(request, 'srchdstk/detalheBusca.html', context)
    
def detalheRepo(request, repo_id):
    # traz detalhes da busca
    repoObj = Repositorio.objects.get(pk=repo_id)
    
    # Monta contexto para passar para o template
    context = {
        'repo': repoObj,
    }

    # Retorna o resultado no template
    return render(request, 'srchdstk/detalheRepo.html', context)
    

def buscaRepos(request):
    repositorio = Repositorio()
    # Ambiente para response
    context = repositorio.busca_repos_no_git()
    return render(request, 'srchdstk/buscaRepos.html', context)

class LinguagemDetail(generic.DetailView):
    model = Linguagem
    context_objects_name = 'linguagem'
    
    #def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        #context = super(LinguagemDetail, self).get_context_data(**kwargs)
        #return context
    
class LinguagemList(generic.ListView):
    model = Linguagem
    def get_queryset(self):
        return Linguagem.objects.all()
    
class LinguagemCreate(generic.edit.CreateView):
    model = Linguagem
    form_class = LinguagemForm

class LinguagemDelete(generic.edit.DeleteView):
    model = Linguagem
    success_url = reverse_lazy('srchdstk:linguagem-list')    