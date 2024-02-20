from django.contrib import admin
from .models import TipoEntrenamiento, Perfil, Nivel, PlanEntrenamiento, Ejercicio, GrupoMuscular, PlanEjercicio, EjercicioRecuperacion, PlanEjercicioRecuperacion, PlanNutricional

admin.site.register(TipoEntrenamiento)

admin.site.register(Perfil)

admin.site.register(Nivel)

admin.site.register(PlanEntrenamiento)

admin.site.register(Ejercicio)

admin.site.register(GrupoMuscular)

admin.site.register(PlanEjercicio)

admin.site.register(EjercicioRecuperacion)

admin.site.register(PlanEjercicioRecuperacion)

admin.site.register(PlanNutricional)