import unittest
from django.test import TestCase, Client
from django.urls import reverse

from .models import Linguagem, Busca, Repositorio

def create_linguagem(linguagem_nome):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    return Linguagem.objects.create(linguagem_nome=linguagem_nome)

        
class SiteIndexTests(TestCase):
    def test_sem_linguagem(self):
        """
        Se não tiverem linguagens cadastradas, deve aparecer uma mensagem "Não há buscas..." na Index
        """
        response = self.client.get(reverse('srchdstk:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não há buscas realizadas!")
        self.assertQuerysetEqual(response.context['lista_repos'], [])
        
    def test_com_linguagem_sem_busca(self):
        """
        Tem linguagens cadastradas, mas não foram feitas buscas
        """
        create_linguagem(linguagem_nome="Java")
        response = self.client.get(reverse('srchdstk:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não há buscas realizadas!")
        self.assertQuerysetEqual(response.context['lista_repos'], [])

class RepositoriosTests(TestCase):
    def test_busca_repositorios_sem_linguagens(self):
        """
        Busca repositórios, mas não tem linguagens cadastradas
        """
        #create_linguagem(linguagem_nome="Java")
        response = self.client.get(reverse('srchdstk:buscaRepos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Busca não retornou resultados!")
        
    def test_busca_repositorios_com_linguagem(self):
        """
        Busca repositórios, com uma linguagem cadastrada
        """
        create_linguagem(linguagem_nome="Java")
        response = self.client.get(reverse('srchdstk:buscaRepos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Qtde de Repositórios")
        
        