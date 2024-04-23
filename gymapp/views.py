from django.shortcuts import render, redirect, get_object_or_404
from .models import Perfil,Equipamiento_Del_Usuario
from .forms import SignUpForm,CustomAuthenticationForm, PerfilForm, EquipamientoForm
from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def signin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'index.html', {'form': form})

def home(request):
    return render(request,'home.html')

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            return redirect('go/')
        else:
            # Si el formulario no es válido, renderiza el formulario nuevamente con los errores
            return render(request, 'sign-up.html', {'form': form})

    # Si es una solicitud GET, simplemente renderiza el formulario vacío
    return render(request, 'sign-up.html', {'form': form})

def signupgo(request):
    if request.method == 'POST':
        name = request.POST.get('nm')
        apellido = request.POST.get('apll')
        naci = request.POST.get('btd')
        condiciones = request.POST.get('med')
        peso = float(request.POST.get('wgt'))
        objetivos = request.POST.get('objt')
        altura = float(request.POST.get('hgt'))
        estado = int(request.POST.get('phy'))
        genero = request.POST.get('gnd')
        deporte = request.POST.get('spt')
        form_data = request.session.get('form_data')
        naci = datetime.strptime(naci, '%Y-%m-%d').date()
        if form_data:
            form = SignUpForm(form_data)
            if form.is_valid():
                form = form.save()
                perfil = Perfil.objects.create(
                user=form,
                peso=peso,
                altura=altura,
                condicion_fisica=estado,
                objetivos=objetivos,
                genero=genero,
                nombre=name,
                apellido=apellido,
                condiciones_medicas=condiciones,
                deporte_practicado=deporte,
                fecha_de_registro = datetime.now(),
                fecha_Nacimiento = naci


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
@login_required
def logout_view(request):
    if request.method == 'POST':
        django_logout(request)
        return redirect('/')
@login_required
def main(request):
    return render(request, 'mainPage.html')

@login_required
def profile(request):
    if request.method == 'GET':
        perfil = get_object_or_404(Perfil,user = request.user)
        form = PerfilForm(instance=perfil)
        return render(request,'profile.html',{'perfil' : perfil,'form':form} )
    else:
        perfil = get_object_or_404(Perfil,user = request.user)
        form = PerfilForm(request.POST, instance=perfil)
        form.save()
        return redirect('main')

@login_required
def equipment(request):
    if request.method == 'GET':
        try:
            Equipamiento_Del_Usuario.objects.get(user = request.user)
        except ObjectDoesNotExist:
            Equipamiento_Del_Usuario.objects.create(user=request.user, equp_gimnasio= '', equp_casa='')
        equipamiento = Equipamiento_Del_Usuario.objects.get(user = request.user)
        form = EquipamientoForm(instance=equipamiento)
        return render(request,'equipo.html',{'perfil' : equipamiento,'form':form} )
    else:
        equipamiento = get_object_or_404(Equipamiento_Del_Usuario,user = request.user)
        form = EquipamientoForm(request.POST, instance=equipamiento)
        form.save()
        print(form)
        return redirect('main')
    
        