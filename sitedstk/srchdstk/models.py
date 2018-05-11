from django.db import models

class Linguagem(models.Model):
    linguagem_nome = models.CharField(max_length=40)
    def __str__(self):
        return self.linguagem_nome
    
class Busca(models.Model):
    linguagem = models.ForeignKey(Linguagem, on_delete=models.CASCADE)
    data_busca = models.DateTimeField('data da busca')
    
    def __str__(self):
        return "{0} {1}".format( self.linguagem.linguagem_nome, self.data_busca )

class Repositorio(models.Model):
    linguagem = models.ForeignKey(Linguagem, on_delete=models.CASCADE)
    data_busca = models.ForeignKey(Busca, on_delete=models.CASCADE)
    repo_id = models.BigIntegerField(default=0)
    repo_name = models.CharField(max_length=256)
    repo_full_name = models.CharField(max_length=540)
    repo_url = models.URLField(null=True)
    repo_description = models.TextField(null=True)
    repo_language = models.CharField(max_length=40)
    repo_score = models.FloatField(null=True)
    repo_stargazers_count = models.FloatField(null=True)