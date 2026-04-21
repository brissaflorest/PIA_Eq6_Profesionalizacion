from django.shortcuts import render
from .models import Servicio

# Create your views here.
def servicio_list(request):
    servicios = Servicio.objects.all()
    return render(request, 'Pia_Eq6.html', {'servicios': servicios})
