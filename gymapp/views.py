from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil
from .forms import SignUpForm

# Create your views here.

def home(request):
    return render(request, 'index.html')


#def signup(request):
    if request.method == 'POST':
        # Creamos un formulario de registro con los datos enviados por el usuario
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Creamos un nuevo usuario de Django
            user = form.save()
            # Creamos un perfil asociado al usuario
            perfil = Perfil.objects.create(
                user=user,
                peso=form.cleaned_data['peso'],
                altura=form.cleaned_data['altura'],
                dias_entrenando=form.cleaned_data['dias_entrenando'],
                experiencia_entrenamiento=form.cleaned_data['experiencia_entrenamiento'],
                edad=form.cleaned_data['edad'],
                objetivos=form.cleaned_data['objetivos'],
                tipo_entrenamiento=form.cleaned_data['tipo_entrenamiento']
            )
            # Redireccionamos al usuario a alguna página de éxito, por ejemplo, el home
            return redirect('home')
    else:
        # Si es un método GET, simplemente mostramos el formulario de registro vacío
        form = SignUpForm()
    return render(request, 'sign-up.html', {'form': form})

#def signup(request):
    form = UserCreationForm()
    return render(request,'sign-up.html',{'form':form})
def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('username'))
            request.session['form_data'] = form.cleaned_data
            return redirect('go/')
        else:
            # Si el formulario no es válido, renderiza el formulario nuevamente con los errores
            return render(request, 'sign-up.html', {'form': form})

    # Si es una solicitud GET, simplemente renderiza el formulario vacío
    return render(request, 'sign-up.html', {'form': form})

def signupgo(request):
    if request.method == 'POST':
        
        peso = float(request.POST.get('wgt'))
        objetivos = request.POST.get('objt')
        altura = float(request.POST.get('hgt'))
        frecuencia = int(request.POST.get('fre'))
        experiencia = int(request.POST.get('exp'))
        genero = request.POST.get('gnd')
        edad = int(request.POST.get('age'))
        form_data = request.session.get('form_data')
        if form_data:
            form = SignUpForm(form_data)
            if form.is_valid():
                form = form.save()
                perfil = Perfil.objects.create(
                user=form,
                peso=peso,
                altura=altura,
                dias_entrenando=frecuencia,
                experiencia_entrenamiento=experiencia,
                edad=edad,
                objetivos=objetivos,
                genero=genero
            )
                return redirect('/')
    else:

        form_data = request.session.get('form_data')
        print(form_data)
        if form_data:
            
            form = SignUpForm(form_data)
            if form.is_valid():
                print(True)
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                return render(request, 'sign-up-go.html',{'username': username, 'password': password, 'email':email})
            else:
                 return redirect('/accounts/sign-up/')
        else:
            return redirect('/accounts/sign-up/')

def options(request):
    return render(request, 'options.html')