from django.shortcuts import render, redirect, get_object_or_404
from .models import Perfil,Equipamiento_Del_Usuario,DietaDiaria, Macros
from .forms import SignUpForm,CustomAuthenticationForm, PerfilForm, EquipamientoForm, DietaDiariaForm
from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from gymapp.testApi import get_completion, macrosCalc, calcular_edad

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

@login_required
def dietBot(request):
    form = DietaDiariaForm()  # Crea una instancia del formulario DietaDiariaForm

    if request.method == 'POST':
        if request.POST.get('action') == 'GUARDAR':  # Verifica si se envió la opción 'GUARDAR'
            # Crea una instancia del formulario DietaDiariaForm con los datos del request.POST
            form = DietaDiariaForm(request.POST)

            
            if form.is_valid():
                comida1 = form.cleaned_data.get('comida1')
                comida2 = form.cleaned_data.get('comida2')
                comida3 = form.cleaned_data.get('comida3')
                comida4 = form.cleaned_data.get('comida4')
                comida5 = form.cleaned_data.get('comida5')
                comida6 = form.cleaned_data.get('comida6')
                DietaDiaria.objects.create(user=request.user,comida1=comida1,comida2=comida2,comida3=comida3,comida4=comida4,comida5=comida5,comida6=comida6,fecha= datetime.now())
                return redirect('main')
        user_input = request.POST.get('user_input')
        solicitud = f"""Quiero que actúes como un nutricionista que sabe muchos platillos distintos. Necesito que me des 6 comidas para un día completo teniendo en cuenta que solamente quiero respuestas sencillas, el formato con el que me vas a responder quiero que sea el siguiente: 
Desayuno: Tu respuesta,Almuerzo: Tu respuesta,Merienda: Tu respuesta,Cena: Tu respuesta,Snack: Tu respuesta,Postre: Tu respuesta
Aparte de esto quiero que tú nunca uses, comas, paréntesis ni comillas en tus respuestas y solamente quiero que seas conciso con lo que te pido y me des lo que necesito.
Ahora quiero que bases tus respuestas en esto: {user_input}"""
        respuesta = get_completion(solicitud)
        comidas = respuesta.split(',')
        # Crear un diccionario con las comidas generadas para inicializar el formulario
        initial_data = {}
        for i, comida in enumerate(comidas, start=1):
            initial_data[f'comida{i}'] = comida.strip()
        # Crear una instancia del formulario DietaDiariaForm con las comidas generadas como datos iniciales
        form = DietaDiariaForm(initial=initial_data)
        

    # Renderizar la plantilla dieta.html con el formulario en el contexto
    
    return render(request, 'dieta.html', {'form': form})

@login_required
def macros(request):
    
    perfil = Perfil.objects.get(user = request.user)
    ejer = perfil.condicion_fisica
    fechaN = perfil.fecha_Nacimiento
    edad = calcular_edad(fechaN)
    obj = perfil.objetivos
    alt=perfil.altura
    peso=perfil.peso
    genero = perfil.genero
    if request.method == 'GET':

        return render(request, 'macrosCalc.html',{'ejer' : ejer, 'peso':peso, 'alt':alt, 'gn':genero, 'age':edad, 'obj':obj})
    else:
        peso = float(request.POST.get('wgt'))
        alt = float(request.POST.get('hgt'))
        act = int(request.POST.get('phy'))
        edad = int(request.POST.get('age'))
        goal = request.POST.get('goal')
        genero = request.POST.get('gnd')
        calorias = macrosCalc(peso,alt,edad,act,goal,genero)
        p1 = calorias*0.4
        p1 = round((p1/4),1)
        p2 = calorias*0.3
        p2 = round((p2/4),1)
        p3 = calorias*0.3
        p3 = round((p3/9),1)
        calorias = round(calorias,1)
        
        print(p1)
        print(p2)
        print(p3)
        print(calorias)
            
        p,coso = Macros.objects.update_or_create(
                    user=request.user,
                    defaults={'proteinas': p1, 'grasas': p3, 'carbohidratos': p2, 'calorias': calorias},
                )
            
        
        return render(request, 'macrosCalc.html', {'ejer' : ejer, 'peso':peso, 'alt':alt, 'gn':genero, 'result':calorias, 'proteinas':p1, 'grasas':p3, 'carboH':p2, 'age':edad, 'obj':goal})

@login_required
def rutinas(request):
    return render(request, 'rutinas.html')