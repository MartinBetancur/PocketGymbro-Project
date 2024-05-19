from django.contrib import admin
from .models import  Perfil, Historial, DietaDiaria, Equipamiento_Del_Usuario, Lesiones, Macros

admin.site.register(Perfil)
admin.site.register(Historial)
admin.site.register(DietaDiaria)
admin.site.register(Equipamiento_Del_Usuario)
admin.site.register(Lesiones)
admin.site.register(Macros)