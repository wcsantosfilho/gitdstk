from django.test import TestCase
from .models import Linguagem
from django.urls import reverse

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
        Se não tiverem linguagens cadastradas, deve aparecer uma mensagem de erro na Index
        """
        response = self.client.get(reverse('srchdstk:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['lista_repos'], [])