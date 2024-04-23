from django.contrib.auth.models import User
from django.db import models
from datetime import date


class CondicionFisica(models.IntegerChoices):
    UNO = 1, '1'
    DOS = 2, '2'
    TRES = 3, '3'
    CUATRO = 4, '4'
    CINCO = 5, '5'
    SEIS = 6, '6'
    SIETE = 7, '7'
    OCHO = 8, '8'
    NUEVE = 9, '9'
    DIEZ = 10, '10'



class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.TextField(default=None)
    apellido = models.TextField(default='', null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    condicion_fisica = models.IntegerField(choices=CondicionFisica.choices, default=None)
    fecha_Nacimiento = models.DateField(default=None)
    def calcular_edad(self):
        today = date.today()
        edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return edad

    edad = property(calcular_edad)
    objetivos = models.TextField(default=None)
    genero = models.TextField(default=None)
    deporte_practicado = models.TextField(default=None)
    fecha_de_registro = models.DateField(default=None)
    condiciones_medicas = models.TextField(default=None)


    def __str__(self):
        return self.user.username

class Historial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha = models.DateField(default=None)
    rutina = models.TextField(default=None)
    duracion = models.TimeField(default=None)
    lesiones = models.TextField(default=None)
    opinion = models.IntegerField(choices=CondicionFisica.choices)
    
class DietaDiaria(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comida1 = models.TextField(default=None)
    comida2 = models.TextField(default=None)
    comida3 = models.TextField(default=None)
    comida4 = models.TextField(default=None)
    comida5 = models.TextField(default=None)
    comida6 = models.TextField(default=None)
    fecha = models.DateField(default=None)

class Equipamiento_Del_Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equp_gimnasio = models.TextField(default=None)
    equp_casa = models.TextField(default=None)

class Lesiones(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lesion = models.TextField(default=None)
