from django.http import HttpResponse
from django.template import loader

from .models import Linguagem

def index(request):
    search_ling = Linguagem.objects.order_by('linguagem_nome')
    template = loader.get_template('srchdstk/index.html')
    context = {
        'search_ling':search_ling,
    }
    return HttpResponse(template.render(context, request))

def detail(request, linguagem_id):
    return HttpResponse("Esta é a linguagem %s" % linguagem_id)
