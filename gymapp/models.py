from django.contrib.auth.models import User
from django.db import models


#Esta clase define los diferentes tipos de entrenamiento que ofrece la aplicación, como ganar rapidez, fuerza, hipertrofia o vida sana.
class TipoEntrenamiento(models.Model):
    TIPO_VELOCIDAD = 'VE'
    TIPO_FUERZA = 'FU'
    TIPO_HIPERTROFIA = 'HI'
    TIPO_SALUD = 'SA'
    TIPOS = [
        (TIPO_VELOCIDAD, 'Velocidad'),
        (TIPO_FUERZA, 'Fuerza'),
        (TIPO_HIPERTROFIA, 'Hipertrofia'),
        (TIPO_SALUD, 'Salud'),
    ]
    nombre = models.CharField(max_length=2, choices=TIPOS)

    def __str__(self):
        return self.get_nombre_display()


#Esta clase representa el perfil de un usuario, que incluye su peso, altura, días de entrenamiento, experiencia de entrenamiento, edad y objetivos. Además, se asocia a un usuario de Django y a un tipo de entrenamiento.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    dias_entrenando = models.IntegerField()
    experiencia_entrenamiento = models.IntegerField()
    edad = models.IntegerField()
    objetivos = models.TextField()
    tipo_entrenamiento = models.ForeignKey(TipoEntrenamiento, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


#Esta clase define los diferentes niveles de dificultad de los planes de entrenamiento, como principiante, intermedio y avanzado.
class Nivel(models.Model):
    NIVEL_1 = 'N1'
    NIVEL_2 = 'N2'
    NIVEL_3 = 'N3'
    NIVELES = [
        (NIVEL_1, 'Principiante'),
        (NIVEL_2, 'Intermedio'),
        (NIVEL_3, 'Avanzado'),
    ]
    nombre = models.CharField(max_length=2, choices=NIVELES)

    def __str__(self):
        return self.get_nombre_display()


#Esta clase representa un plan de entrenamiento personalizado para un usuario. Se asocia a un perfil de usuario, un nivel de dificultad y un tipo de entrenamiento. Además, se pueden asociar varios ejercicios y ejercicios de recuperación a un plan de entrenamiento.
class PlanEntrenamiento(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    dias_semana = models.IntegerField()
    tipo_entrenamiento = models.ForeignKey(TipoEntrenamiento, on_delete=models.CASCADE)
    ejercicios = models.ManyToManyField('Ejercicio', through='PlanEjercicio')
    ejercicios_recuperacion = models.ManyToManyField('EjercicioRecuperacion', through='PlanEjercicioRecuperacion')

    def __str__(self):
        return f"{self.usuario} - {self.nivel} - {self.tipo_entrenamiento} - {self.dias_semana} días"


#Esta clase representa un ejercicio que se puede incluir en un plan de entrenamiento. Incluye un nombre, una descripción y los grupos musculares que involucra.
class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    grupos_musculares = models.ManyToManyField('GrupoMuscular')

    def __str__(self):
        return self.nombre


#Esta clase representa un grupo muscular, como bíceps, tríceps, pecho, espalda, etc. Se asocia a varios ejercicios.
class GrupoMuscular(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


#Esta clase representa una asociación entre un plan de entrenamiento y un ejercicio, y especifica el número de series y repeticiones para ese ejercicio en ese plan de entrenamiento.
class PlanEjercicio(models.Model):
    plan = models.ForeignKey(PlanEntrenamiento, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    serie = models.IntegerField()
    repeticiones = models.IntegerField()
    orden = models.IntegerField()

    def __str__(self):
        return f"{self.plan} - {self.ejercicio} - {self.serie} x {self.repeticiones}"


#Esta clase representa un ejercicio de recuperación que se puede incluir en un plan de entrenamiento. Incluye un nombre, una descripción y los grupos musculares que involucra.
class EjercicioRecuperacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    grupos_musculares = models.ManyToManyField('GrupoMuscular')

    def __str__(self):
        return self.nombre


#Esta clase representa una asociación entre un plan de entrenamiento y un ejercicio de recuperación, y especifica el día en que se debe realizar ese ejercicio de recuperación.
class PlanEjercicioRecuperacion(models.Model):
    plan = models.ForeignKey(PlanEntrenamiento, on_delete=models.CASCADE)
    ejercicio_recuperacion = models.ForeignKey(EjercicioRecuperacion, on_delete=models.CASCADE)
    dia = models.IntegerField()

    def __str__(self):
        return f"{self.plan} - {self.ejercicio_recuperacion} - Día {self.dia}"


#Esta clase representa un plan nutricional personalizado para un plan de entrenamiento. Se asocia a un plan de entrenamiento y contiene una descripción de la dieta recomendada.
class PlanNutricional(models.Model):
    plan_entrenamiento = models.OneToOneField(PlanEntrenamiento, on_delete=models.CASCADE)
    dieta = models.TextField()

    def __str__(self):
        return f"Plan Nutricional para {self.plan_entrenamiento.usuario}"
    