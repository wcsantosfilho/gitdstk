from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Max, Count, F
from django.contrib import messages
import requests
import json
import re

from .models import Linguagem, Busca, Repositorio

def index(request):
    # monta lista com ID das linguagens
    lista_linguagens = Linguagem.objects.all()
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
        'lista_buscas': lista_buscas,
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
    # Ambiente para response
    context = {}

    # Monta lista com todas as linguagens da tabela
    lista_ling = Linguagem.objects.all()
    
    # Salva a DataHora da Busca
    dataHoraBusca = timezone.now()
    
    # Apenas teste!!
    dict_repo1 = dict()
    
    # Loop para chamar o API do GIt para cada uma das Linguagens
    for ling in lista_ling:
        busca = Busca(linguagem=ling, data_busca=dataHoraBusca)
        busca.save()
        urlGit = "https://api.github.com/search/repositories?q=language:" + ling.linguagem_nome + "&sort=stars&order=desc"
        headerGit = {'Accept': 'application/vnd.github.mercy-preview+json'}
        try:
            gitResposta = requests.get(urlGit,headers=headerGit)

            #Testa sucesso da resposta
            if (gitResposta.ok):
                # Carrega conteudo JSON
                jsonGit = json.loads(gitResposta.content)
                
                # Verifica a qtde de itens da resposta
                itensGit = int(jsonGit['total_count'])
                if (itensGit > 0):
                    count = 0
                    dict_repo2 = dict()
                    for key in range(0, itensGit):
                        # adiciona algumas keys ao dict da linguagem
                        dict_repo3 = dict()
                        dict_repo3['id'] = jsonGit['items'][key]['id']
                        dict_repo3['name'] = jsonGit['items'][key]['name']
                        dict_repo3['full_name'] = jsonGit['items'][key]['full_name']
                        dict_repo3['url'] = jsonGit['items'][key]['url']
                        dict_repo3['description'] = jsonGit['items'][key]['description']
                        dict_repo3['language'] = jsonGit['items'][key]['language']
                        dict_repo3['score'] = jsonGit['items'][key]['score']
                        dict_repo3['stargazers_count'] = jsonGit['items'][key]['stargazers_count']
                        dict_repo2[key] = dict_repo3
                        temp_description = re.sub(r'[^\x00-\x7F]+',' ',jsonGit['items'][key]['description'])
                        repo = Repositorio(linguagem=ling, busca=busca, repo_id = jsonGit['items'][key]['id'], repo_name = jsonGit['items'][key]['name'], repo_full_name = jsonGit['items'][key]['full_name'], repo_url = jsonGit['items'][key]['html_url'], repo_description = temp_description , repo_language = jsonGit['items'][key]['language'], repo_score = jsonGit['items'][key]['score'], repo_stargazers_count = jsonGit['items'][key]['stargazers_count'] )
                        repo.save()
                        count = count + 1
                        if (count > 5):
                            break
                    # adiciona ao dict dos repositórios
                    dict_repo1[ling] = dict_repo2
                
                # Monta contexto para passar para o template
                context = { 
                    'dict_repo1': dict_repo1
                }
            else:
                gitResposta.raise_for_status()
        except requests.exceptions.RequestException as e:
            print (e)
    return render(request, 'srchdstk/buscaRepos.html', context)

