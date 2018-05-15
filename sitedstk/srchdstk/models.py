from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.urls import reverse
import requests
import json
import re


class Linguagem(models.Model):
    linguagem_nome = models.CharField(max_length=40)
    
    def get_absolute_url(self):
        return reverse('srchdstk:linguagem-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.linguagem_nome
    
class LinguagemForm(ModelForm):
    class Meta:
        model = Linguagem
        fields = ['linguagem_nome']
    
class Busca(models.Model):
    linguagem = models.ForeignKey(Linguagem, on_delete=models.CASCADE)
    data_busca = models.DateTimeField('data da busca')
    
    def __str__(self):
        return "{0}: {1} | {2}".format( self.id, self.linguagem.linguagem_nome, self.data_busca )

class Repositorio(models.Model):
    linguagem = models.ForeignKey(Linguagem, on_delete=models.CASCADE)
    busca = models.ForeignKey(Busca, on_delete=models.CASCADE)
    repo_id = models.BigIntegerField(default=0)
    repo_name = models.CharField(max_length=256)
    repo_full_name = models.CharField(max_length=540)
    repo_url = models.URLField(null=True)
    repo_description = models.TextField(null=True)
    repo_language = models.CharField(max_length=40)
    repo_score = models.FloatField(null=True)
    repo_stargazers_count = models.FloatField(null=True)
    
    def __str__(self):
        return "{0} | {1} | {2} | {3} | {4}".format( self.linguagem.linguagem_nome, self.busca.data_busca, self.repo_full_name, self.repo_description, self.id )
    
    def busca_repos_no_git(self):
        # ----------------------------------------------------------------------------------------
        # Pesquisa Repositorios no GitHub das linguagens cadastradas e retorna as N mais populares
        # Monta um dicionário com o resultado da busca
        # -----------------------------------------------------------------------------------------
        context = {}
        # Monta lista com todas as linguagens da tabela
        lista_ling = Linguagem.objects.all()

        # Salva a DataHora da Busca
        dataHoraBusca = timezone.now()

        # Dicionário com o resultado
        dict_repo1 = dict()

        # Loop para chamar o API do GIt para cada uma das Linguagens
        for ling in lista_ling:
            try:
                busca = Busca(linguagem=ling, data_busca=dataHoraBusca)
                busca.save()
                urlGit = "https://api.github.com/search/repositories?q=language:" + ling.linguagem_nome + "&sort=stars&order=desc"
                headerGit = {'Accept': 'application/vnd.github.mercy-preview+json'}
                try:
                    gitResposta = requests.get(urlGit,headers=headerGit)

                    #Testa sucesso da resposta
                    count_repos = 0
                    if (gitResposta.ok):
                        # Carrega conteudo JSON
                        jsonGit = json.loads(gitResposta.content)

                        # Verifica a qtde de itens da resposta
                        itensGit = int(jsonGit['total_count'])
                        if (itensGit > 0):
                            for key in range(0, itensGit):
                                temp_description = re.sub(r'[^\x00-\x7F]+',' ',jsonGit['items'][key]['description'])
                                repo = Repositorio(linguagem=ling, busca=busca, repo_id = jsonGit['items'][key]['id'], repo_name = jsonGit['items'][key]['name'], repo_full_name = jsonGit['items'][key]['full_name'], repo_url = jsonGit['items'][key]['html_url'], repo_description = temp_description , repo_language = jsonGit['items'][key]['language'], repo_score = jsonGit['items'][key]['score'], repo_stargazers_count = jsonGit['items'][key]['stargazers_count'] )
                                try:
                                    repo.save()
                                except Error as e:
                                    print(e)
                                count_repos = count_repos + 1
                                if (count_repos > 4):
                                    break

                        # Monta contexto para passar para o template
                        context = { 
                            'dict_repo1': dict_repo1
                        }
                    #else:
                        #gitResposta.raise_for_status()
                    # adiciona ao dict dos repositórios
                    dict_repo1[ling] = count_repos

                except requests.exceptions.RequestException as e:
                    print (e)
            except Error as e:
                print(e)
        return context
