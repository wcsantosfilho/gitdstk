from django.db import models

class Linguagem(models.Model):
    linguagem_nome = models.CharField(max_length=40)
    def __str__(self):
        return self.linguagem_nome
    
class Search(models.Model):
    linguagem = models.ForeignKey(Linguagem, on_delete=models.CASCADE)
    search_date = models.DateTimeField('data do search')
    