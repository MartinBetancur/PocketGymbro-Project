from django.shortcuts import render, redirect, get_object_or_404
from .models import Perfil,Equipamiento_Del_Usuario,DietaDiaria, Macros, Dieta_Semanal,Historial,Lesiones
from .forms import SignUpForm,CustomAuthenticationForm, PerfilForm, EquipamientoForm, DietaDiariaForm
from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from gymapp.testApi import get_completion, macrosCalc, calcular_edad, repuestaJson
from .forms import EvaluacionRutinaForm
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
        if request.POST.get('action') == 'Save':  # Verifica si se envió la opción 'GUARDAR'
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
        try:
            data_macros = Macros.objects.get(user = request.user)
            proteinas = data_macros.proteinas
            grasas = data_macros.grasas
            carbohidratos = data_macros.carbohidratos
            solicitud = f"""Quiero que actúes como un nutricionista que sabe muchos platillos distintos. Necesito que me des 6 comidas para un día completo teniendo en cuenta que solamente quiero respuestas sencillas, el formato con el que me vas a responder quiero que sea el siguiente: 
Desayuno: Tu respuesta,Almuerzo: Tu respuesta,Merienda: Tu respuesta,Cena: Tu respuesta,Snack: Tu respuesta,Postre: Tu respuesta
Aparte de esto quiero que tú nunca uses, comas, paréntesis ni comillas en tus respuestas y solamente quiero que seas conciso con lo que te pido y el formato que te doy, recuerda solamente utilizar comas para separar las comidas del dia y me des lo que necesito.
Ahora quiero que bases tus respuestas en esto: {user_input} quiero que tengas en cuenta las macros de la persona que son las siguientes: las proteinas recomendandas del usuario son {proteinas}gramos, los carbohidratos recomendados son {carbohidratos} gramos y las grasas recomendadas son {grasas} gramos"""
        except ObjectDoesNotExist:
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
            
        p,coso = Macros.objects.update_or_create(
                    user=request.user,
                    defaults={'proteinas': p1, 'grasas': p3, 'carbohidratos': p2, 'calorias': calorias},
                )
            
        
        return render(request, 'macrosCalc.html', {'ejer' : ejer, 'peso':peso, 'alt':alt, 'gn':genero, 'result':calorias, 'proteinas':p1, 'grasas':p3, 'carboH':p2, 'age':edad, 'obj':goal})

@login_required
def rutinas(request):
    if request.method == 'POST':
        
        if request.POST.get('action') == 'Go':
            pass
        user_input = request.POST.get('user_input')
        place = request.POST.get('place')
        perfil = Perfil.objects.get(user = request.user)
        deporte = perfil.deporte_practicado
        objetivo = perfil.objetivos
        condiciones = perfil.condiciones_medicas
        genero = perfil.genero
        edad = perfil.fecha_Nacimiento
        edad = calcular_edad(edad)
        try:
            equipa = Equipamiento_Del_Usuario.objects.get(user = request.user)
            if place == 'Gym':
                equipa = equipa.equp_gimnasio
                if equipa == '':
                    equipa = 'No especificado'
                
            else:
                equipa = equipa.equp_casa
                if equipa == '':
                    equipa = 'No especificado'
        except ObjectDoesNotExist:
            equipa = 'No especificado'
        solicitud = '''Necesito que actues como un entrenador deportivo de alta calidad, tu proposito es dar excelente rutinas de ejercicio para las personas dependiendo de las distintas caracteristicas de la persona en si. La rutina que vas a proporcionar va a ser en formato json de la manera que te voy a decir a continuación: {"Tiempo_Aproximado" : "Tu respuesta", "Tiempo_de_Descanso": "Tu respuesta", "Calentamiento" : "Tu respuesta" , "Numero_de_series_por_ejercicio" : "Tu respuesta", "Ejercicios" : {"Ejercicio_1": "Tu respuesta", "Ejercicio_2": "Tu respuesta", "Ejercicio_3": "Tu respuesta - Numero de repeticiones", "Ejercicio_4": "Tu respuesta ", "Ejercicio_5": "Tu respuesta", "Ejercicio_6": "Tu respuesta",.....,"Ejercicio_n":"Tu respuesta"}}

'''+ f'''Las caracteristicas de la persona son las siguientes: Genero: {genero}, Objetivo: {objetivo}, Edad: {edad} años, Condiciones medicas: {condiciones}, Deporte practicado: {deporte}, Equipamiento para entrenar: {equipa}, Lugar de entreno: {place}
La cantidad de ejercicios depende de tu criterio o de lo que la persona especifique, lo mismo con la el tiempo aproximado y el tiempo de descanso. Estas son las cualidades especificas que quiere la persona en su rutina: {user_input}. Dado el caso que la persona no especifique nada, o lo que te haya dicho no tenga nada de relevancia, elige por ella lo mas adecuado basado en los datos que se te han dado.

Por ultimo solamente quiero que la respuesta que me des sea el json, no quiero que me des ningun mensaje mas para que des un mejor rendimiento.'''
        respuestaVanilla = get_completion(solicitud)
        respuestaDict = repuestaJson(respuestaVanilla)
        print(respuestaDict["Tiempo_Aproximado"])

        return render(request, 'rutinas.html', {'respuestaV': respuestaVanilla, 'entreno': respuestaDict})
    else:

        return render(request, 'rutinas.html')

@login_required
def semanalDieta(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'Save':
            jsonsito = request.POST.get('r') 
            jsonsito = repuestaJson(jsonsito)
            
            Dieta_Semanal.objects.update_or_create(user = request.user, defaults={'horario':jsonsito})
            return redirect('main')
            
            
        user_input = request.POST.get('user_input')
        try:
            data_macros = Macros.objects.get(user = request.user)
            proteinas = data_macros.proteinas
            grasas = data_macros.grasas
            carbohidratos = data_macros.carbohidratos
            solicitud = """Quiero que actues como nutricionista deportivo, sabes lo que son las macros de una persona y lo que deberia comer en el dia. Quiero que me des en un formato Json como este: {"Lunes":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Martes":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Miercoles":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Jueves":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Viernes":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Sabado":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Domingo":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}}

En donde dice "Tu respuesta" tu vas a darme una recomendacion para comer basada en lo siguiente:""" + f""" {user_input}, Ademas quiero que tengas en cuenta las macros de la persona que son las siguientes: las proteinas recomendandas del usuario son {proteinas}gramos, los carbohidratos recomendados son {carbohidratos} gramos y las grasas recomendadas son {grasas} gramos.
Recuerda que no quiero que me des cualquier otro tipo de respuesta aparte del Json"""
        except ObjectDoesNotExist:
            solicitud = """Quiero que actues como nutricionista deportivo, sabes lo que son las macros de una persona y lo que deberia comer en el dia. Quiero que me des en un formato Json como este: {"Lunes":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Martes":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Miercoles":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Jueves":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Viernes":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Sabado":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}, "Domingo":{"Desayuno":"Tu respuesta", "Almuerzo":"Tu respuesta", "Merienda":"Tu respuesta", "Cena":"Tu respuesta", "Snack":"Tu respuesta", "Postre":"Tu respuesta"}}

En donde dice "Tu respuesta" tu vas a darme una recomendacion para comer basada en lo siguiente:""" + f""" {user_input}.
Recuerda que no quiero que me des cualquier otro tipo de respuesta aparte del Json"""
        respuesta = get_completion(solicitud)
        # Crear un diccionario con las comidas generadas para inicializar el formulario
        x = repuestaJson(respuesta)
        return render(request, 'dietaSemanal.html', {'respuesta': x, 'osea': respuesta})
        
        

    # Renderizar la plantilla dieta.html con el formulario en el contexto
    
    
    return render(request, 'dietaSemanal.html')

@login_required
def vista_dieta(request):
    try:
        x = Dieta_Semanal.objects.get(user= request.user)
        x = x.horario
        return render(request, 'visualDieta.html', {'respuesta': x})

    except ObjectDoesNotExist:
        x = True
        return render(request, 'visualDieta.html', {'error': x})
    
@login_required
def rutina_go(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'Save':
            respuesta_v = repuestaJson(request.POST.get('r'))
            opinion = int(request.POST.get('opinion'))
            lesiones = request.POST.get('lesiones', 'Ninguna')
            comentarios = request.POST.get('comentarios', '')  # Nuevo campo para comentarios

            Historial.objects.create(
                user=request.user,
                fecha=datetime.now(),
                rutina=respuesta_v,
                opinion=opinion,
                lesiones=lesiones,
                comentarios=comentarios  # Guardar comentarios
            )

            if lesiones != 'Ninguna':
                Lesiones.objects.create(user=request.user, lesion=lesiones, estado=False, fecha=datetime.now())

            return redirect('main')

        respuesta_v = request.POST.get('r')
        form = EvaluacionRutinaForm()  # Crear el formulario de evaluación
        return render(request, 'rutinaDid.html', {'r': respuesta_v, 'form': form})  # Pasar el formulario al template
    else:
        return redirect('main')
    

@login_required
def historial_rutinas(request):

    rutinas = Historial.objects.filter(user = request.user)
    if not rutinas:
        
        papadio = True
        return render(request, 'historial_r.html', {'noR': papadio })
    else:
        
        return render(request,'historial_r.html', {'hist':rutinas})
        
@login_required
def chatLesiones(request):
    if request.method == 'POST':
        lesion_id = request.POST.get('lesion_id')
        
        lesion = Lesiones.objects.get(id=lesion_id)
        # Cambiar el estado de la lesión
        lesion.estado = not lesion.estado  # Cambiar entre True y False
        lesion.save()
        return redirect('/main/lesiones/')

        
    else:

        les = Lesiones.objects.filter(user = request.user)
        if not les:
            
            return render(request, 'lesionesBot.html')

        return render(request, 'lesionesBot.html', {'les':les})
    
@login_required
def botLesiones(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'chat':
            res = request.POST.get('user_input')
            les = request.POST.get('lesion')
            solicitud = f'''Quiero que actues como un medico deportivo, y le propongas ejercicios de recuperacion para ciertas lesiones, en este caso la lesion es: {les}, 
        ademas la persona puede que te de detalles extra en este caso son:{res}, si la persona no te da detalles adicionales basate en la lesion antes dada'''
            solicitud = get_completion(solicitud)
            return render(request, 'chatBotLesiones.html', {'respuesta':solicitud})
        les = request.POST.get('lesion')
        
        return render(request, 'chatBotLesiones.html',{'lesion':les})
    else:
        redirect('/main/lesiones/')