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
    DEPORTE_CHOICES = [
        ('SOCCER', 'Soccer'),
        ('BASKETBALL', 'Basketball'),
        ('VOLLEYBALL', 'Volleyball'),
        ('UNDERWATER HOCKEY', 'Underwater Hockey'),
        ('TENNIS', 'Tennis'),
        ('TABLE TENNIS', 'Table Tennis'),
        ('ATHLETICS', 'Athletics'),
        ('CYCLING', 'Cycling'),
        ('CALISTHENICS ', 'Calisthenics'),
        ('HOCKEY ', 'Hockey'),
        ('ARCHERY ', 'Archery'),
        ('OTHER', 'Other'),
        
    ]
    OBJETIVOS_CHOICES = [
        ('MAXIMUM FAT LOSS','Maximum Fat Loss'),
        ('SOME FAT LOSS','Some Fat Loss'),
        ('MANTAIN','Maintain'),
        ('STEADY GAIN','Steady Gain'),
        ('GAIN','Gain'),
    ]
    GENERO_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('NON_BINARY', 'Non-binary'),
        ('TRANSGENDER', 'Transgender'),
        ('GENDERQUEER', 'Genderqueer'),
        ('GENDERFLUID', 'Genderfluid'),
        ('AGENDER', 'Agender'),
        ('BIGENDER', 'Bigender'),
        ('TWO_SPIRIT', 'Two-spirit'),
        ('OTHER', 'Other'),
        ('CISGENDER', 'Cisgender'),
        ('GENDER_QUESTIONING', 'Gender questioning'),
        ('GENDER_NONCONFORMING', 'Gender nonconforming'),
        ('PANGENDER', 'Pangender'),
        ('DEMIBOY', 'Demiboy'),
        ('DEMIGIRL', 'Demigirl'),
        ('ANDROGYNE', 'Androgyne'),
        ('NEUTROIS', 'Neutrois'),
        ('GENDERFLUX', 'Genderflux'),
        ('THIRD_GENDER', 'Third gender'),
        ('BI_GENDER', 'Bi-gender'),
        ('GENDER_EXPANSIVE', 'Gender expansive'),
        ('GENDER_VARIANT', 'Gender variant'),
        ('INTERSEX', 'Intersex'),
        ('THIRD_SEX', 'Third sex'),
        ('MAHORAGA', 'Mahoraga'),
        ('ITACHI', 'Itachi'),
        ('BOEING_AH_64_APACHE', 'Boeing AH-64 Apache'),
        ('GOKU', 'Goku'),
        ('DECEPTICON', 'Decepticon'),
        ('OPTIMUS_PRIME', 'Optimus prime'),
        ('PERRO', 'Perro'),
        ('GATO', 'Gato'),
        ('OBAMA', 'Obama'),
        ('NONE', 'None'),
        ('PREFER_NOT_TO_SAY', 'Prefer Not to Say'),
    ]

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
    objetivos = models.CharField(max_length=21, choices=OBJETIVOS_CHOICES, default='MANTAIN')
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, default='NONE')
    deporte_practicado = models.CharField(max_length=21, choices=DEPORTE_CHOICES, default='OTROS')
    fecha_de_registro = models.DateField(default=None)
    condiciones_medicas = models.TextField(default=None)


    def __str__(self):
        return self.user.username

class Historial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(default=None)
    rutina = models.JSONField()
    lesiones = models.TextField(default=None)
    opinion = models.IntegerField(choices=CondicionFisica.choices)
    
class DietaDiaria(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comida1 = models.CharField(default=None, max_length= 200)
    comida2 = models.CharField(default=None, max_length= 200)
    comida3 = models.CharField(default=None, max_length= 200)
    comida4 = models.CharField(default=None, max_length= 200)
    comida5 = models.CharField(default=None, max_length= 200)
    comida6 = models.CharField(default=None, max_length= 200)
    fecha = models.DateField(default=None)

class Equipamiento_Del_Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equp_gimnasio = models.TextField(default=None)
    equp_casa = models.TextField(default=None)

class Lesiones(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesion = models.TextField(default=None)



class Macros(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    calorias = models.DecimalField(max_digits=10, decimal_places=2)
    proteinas = models.DecimalField(max_digits=10, decimal_places=2)
    grasas = models.DecimalField(max_digits=10, decimal_places=2)
    carbohidratos = models.DecimalField(max_digits=10, decimal_places=2)

class Dieta_Semanal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    horario = models.JSONField()
    

class Rutina_Semanal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    horario = models.JSONField()
    