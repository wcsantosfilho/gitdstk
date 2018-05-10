from django.http import HttpResponse
from .models import Linguagem

def index(request):
    search_ling = Linguagem.objects.order_by('linguagem_nome')
    output = ', '.join([l.linguagem_nome for l in search_ling])
    return HttpResponse(output)

def detail(request, linguagem_id):
    return HttpResponse("Esta é a linguagem %s" % linguagem_id)
