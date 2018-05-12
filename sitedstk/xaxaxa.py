from srchdstk.models import Linguagem, Busca, Repositorio
from django.db.models import Max, Min, Count, F

#lista_linguagens = Linguagem.objects.all()

#for x in lista_linguagens:
#    lb = Busca.objects.all().filter(linguagem_id=x.id).aggregate(Max('data_busca'))
#    print(x.id, "-", x.linguagem_nome, ":", lb.id, "=", lb)
    
zz = Busca.objects.annotate(max_date=Max('linguagem__busca__data_busca')).filter(data_busca=F('max_date'))