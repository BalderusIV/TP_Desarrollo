from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#  Funciones para las vistas del navbar
def compras(req):
    return render(req, "compras.html")

def produccion(request):
    ordenes = Orden.objects.all()
    return render(request, 'produccion.html', {'ordenes': ordenes})

def ventas(req):
    return render(req, "ventas.html")

def deposito(req):
    return render(req, "deposito.html")

def control_calidad(req):
    return render(req, "control_calidad.html")

def inicio(request):
    if request.user.is_authenticated:
        return redirect('App_LUMINOVA:dashboard')  # Redirige al dashboard si está autenticado
    return redirect('App_LUMINOVA:login')  # Redirige al login si no está autenticado

#  Funciones para el login y logout
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard.html')

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect('App_Luminova:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login.html')

#  Funciones para los botones del sidebar del Admin
def usuarios(request):
    return render(request, 'usuarios.html')

def roles_permisos(request):
    return render(request, 'roles_permisos.html')

def auditoria(request):
    return render(request, 'auditoria.html')

#  Funciones para los botones del sidebar de Produccion
def ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'ordenes.html', {'ordenes': ordenes})

def planificacion(request):
    ordenes = Orden.objects.all()
    return render(request, 'planificacion.html', {'ordenes': ordenes})
def reportes(request):
    reportes = Reporte.objects.all()
    return render(request, 'reportes.html', {'reportes': reportes})
def tabla_insumos(request):
    return render(request, 'tabla_insumos.html')

def orden_reporte(request, numero_orden, sector):
    if request.method == 'POST':
        numero_orden = request.POST.get('numero_orden')
        sector = request.POST.get('sector')
        fecha = request.POST.get('fecha')
        tipo_problema = request.POST.get('tipo_problema')
        descripcion = request.POST.get('descripcion')
         
        Reporte.objects.create(
            numero_orden=numero_orden,
            sector=sector,
            fecha=fecha,
            tipo_problema=tipo_problema,
            descripcion=descripcion
        )
        
        return redirect('App_LUMINOVA:reportes')
    fecha_actual = timezone.now().date().strftime('%Y-%m-%d')
    return render(request, 'orden_reporte.html', {
        'numero_orden': numero_orden,
        'sector': sector,
        'fecha_actual': fecha_actual,
    })

def informe_reporte(request):
    return render(request, 'informe_reporte.html')


def actualizar_orden(request, numero_orden):
    orden = get_object_or_404(Orden, numero_orden=numero_orden)
    if request.method == 'POST':
        # Actualiza el sector si viene en el formulario
        if 'sector' in request.POST:
            orden.sector = request.POST.get('sector', orden.sector)
        # Actualiza el estado si viene en el formulario
        if 'estado' in request.POST:
            orden.estado = request.POST.get('estado', orden.estado)
        orden.save()
    return redirect('App_LUMINOVA:planificacion')


def cambiar_estado_orden(request, numero_orden):
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        orden = get_object_or_404(Orden, numero_orden=numero_orden)
        orden.estado = nuevo_estado
        orden.save()
        return redirect('App_LUMINOVA:planificacion')
    
def guardar_cambios_planificacion(request):
    if request.method == 'POST':
        ordenes = Orden.objects.all()
        for orden in ordenes:
            sector = request.POST.get(f'sector_{orden.id}')
            estado = request.POST.get(f'estado_{orden.id}')
            if sector and sector != orden.sector:
                orden.sector = sector
            if estado and estado != orden.estado:
                orden.estado = estado
            orden.save()
    return redirect('App_LUMINOVA:planificacion')