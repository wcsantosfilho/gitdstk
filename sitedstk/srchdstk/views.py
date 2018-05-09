from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World. Aplicativo de search dos destaques do git.")
