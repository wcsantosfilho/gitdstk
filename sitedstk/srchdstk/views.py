from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
import json

from .models import Linguagem, Busca

def index(request):
    # monta lista com ID das linguagens
    lista_id_linguagens = list(Linguagem.objects.all().values_list("id", flat=True))
    # lista buscas feitas com aquela linguagem (JOIN)
    lista_buscas = Busca.objects.filter(linguagem__id__in=lista_id_linguagens)
    # define contexto para passar para o template
    context = {
        'lista_buscas': lista_buscas
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

def buscaRepos(request):
    # Ambiente para response
    context = {}

    # Monta lista com todas as linguagens da tabela
    lista_ling = list(Linguagem.objects.all())
    # Apenas teste!!
    dict_repos = dict()
    
    # Loop para chamar o API do GIt para cada uma das Linguagens
    for ling in lista_ling:
        urlGit = "https://api.github.com/search/repositories?q=glicemia+language:" + ling.linguagem_nome + "&sort=stars&order=desc"
        headerGit = {'Accept': 'application/vnd.github.mercy-preview+json'}
        try:
            gitResposta = requests.get(urlGit,headers=headerGit)
            print (gitResposta.status_code)
            print ("\n")
            print ("Linguagem: ", ling.linguagem_nome)
            print ("\n")

            #Testa sucesso da resposta
            if (gitResposta.ok):
                # Carrega conteudo JSON
                jsonGit = json.loads(gitResposta.content)

                print("A resposta contem {0} item\n".format(jsonGit['total_count']))
                itensGit = int(jsonGit['total_count'])
                if (itensGit > 0):
                    count = 0
                    dict_repo_ling = dict()
                    for key in range(0, itensGit):
                        # adiciona algumas keys ao dict da linguagem
                        dict_repo_ling['full_name'] = jsonGit['items'][key]['full_name']
                        dict_repo_ling['id'] = jsonGit['items'][key]['id']
                        dict_repo_ling['language'] = jsonGit['items'][key]['language']
                        dict_repo_ling['stargazers_count'] = jsonGit['items'][key]['stargazers_count']
                        print(key, " : ", jsonGit['items'][key]['full_name'], "\n")
                        ++count
                        if (count > 5):
                            break
                    # adiciona ao dict dos repositórios
                    dict_repos[ling] = dict_repo_ling
                print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-\n")
                print(dict_repos)
                
                # Monta contexto para passar para o template
                context = { 
                    'dict_repos': dict_repos
                }
            else:
                gitResposta.raise_for_status()
        except requests.exceptions.RequestException as e:
            print (e)
    print("-y-y-y-y-y-y-y-y-y-y-y-y-y-y-\n")
    return render(request, 'srchdstk/buscaRepos.html', context)

