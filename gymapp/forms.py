from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Perfil, Equipamiento_Del_Usuario, DietaDiaria
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre','apellido','peso','altura','condicion_fisica','fecha_Nacimiento','objetivos','genero','deporte_practicado','condiciones_medicas']

class EquipamientoForm(ModelForm):
    class Meta:
        model = Equipamiento_Del_Usuario
        fields = ['equp_gimnasio', 'equp_casa']

class DietaDiariaForm(ModelForm):
    class Meta:
        model = DietaDiaria
        fields = ['comida1','comida2','comida3','comida4','comida5','comida6']