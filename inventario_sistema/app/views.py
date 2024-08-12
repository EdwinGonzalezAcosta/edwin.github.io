import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404, redirect
from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Inventario
from .forms import InventarioForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from PIL import Image as PILImage
import json
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def logout_view(request):
    logout(request)
    return redirect('login')

def my_view(request):
    response = HttpResponse('Contenido protegido')
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    return response

@login_required
def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistroForm()
        form.fields['username'].initial = ''  # Limpia los campos manualmente si es necesario
        form.fields['email'].initial = ''
        form.fields['password1'].initial = ''
        form.fields['password2'].initial = ''

    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print("El formulario no es válido.")
            print(f"Errores: {form.errors}")
    else:
        form = AuthenticationForm()
        print("Se ha mostrado el formulario de inicio de sesión.")

    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto guardado exitosamente.')
            return redirect('home')
        else:
            messages.error(request, 'No se pudo guardar el producto. Verifique los errores del formulario.')
    else:
        form = InventarioForm()
    
    inventory = Inventario.objects.all()
    return render(request, 'home.html', {'inventory': inventory, 'form': form})


@csrf_exempt
def deactivate_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Inventario.objects.get(id=product_id)
            # Obtener el estado desde la solicitud
            data = json.loads(request.body)
            estado_logico = data.get('estado_logico', False)  # Por defecto es False si no está en la solicitud

            # Asegúrate de que estado_logico sea booleano
            if isinstance(estado_logico, int):
                estado_logico = bool(estado_logico)

            product.estado_logico = estado_logico
            product.save()
            return JsonResponse({'success': True})
        except Inventario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def export_to_excel(request):
    # Crea un libro de trabajo de Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Inventario"

    # Define los encabezados de las columnas
    headers = [
        'ID', 'Cod. Patrim.', 'Cod. Interno', 'Año Ingreso', 'Descripción', 'Denominación', 
        'Marca', 'Modelo', 'Color', 'Serie', 'Dimensiones', 
        'Estado', 'Observaciones', 'Imagen'
    ]
    sheet.append(headers)

    # Obtén los datos del inventario
    inventory = Inventario.objects.all()

    # Agrega los datos al archivo Excel
    for index, item in enumerate(inventory, start=2):  # start=2 para comenzar después de los encabezados
        row = [
            item.id, item.cod_patrimonial, item.cod_interno, item.ano_ingreso, item.denominacion,
            item.descripcion.descripcion_inventario, item.marca, 
            item.modelo, item.color, item.serie, item.dimensiones, 
            item.estado_mueble.descripcion_estado, item.observaciones
        ]
        sheet.append(row)

        # Agregar la imagen si existe
        if item.foto:  # Suponiendo que `foto` es el nombre del campo de imagen en tu modelo
            # Convertir la imagen si es .webp a .png
            img_path = item.foto.path
            with PILImage.open(img_path) as img:
                if img.format == 'WEBP':
                    img = img.convert('RGBA')
                    buffer = BytesIO()
                    img.save(buffer, format='PNG')
                    buffer.seek(0)
                    img = Image(buffer)
                else:
                    img = Image(img_path)

            cell = f'N{index}'  # La columna de la imagen es 'N'
            img.width = 100  # Ajusta el tamaño según sea necesario
            img.height = 100  # Ajusta el tamaño según sea necesario
            sheet.add_image(img, cell)

    # Guarda el archivo en un objeto BytesIO
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Configura la respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=inventario.xlsx'

    return response

def export_to_excel_without_images(request):
    # Crea un libro de trabajo de Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Inventario"

    # Define los encabezados de las columnas
    headers = [
        'ID', 'Cod. Patrim.', 'Cod. Interno', 'Año Ingreso', 'Descripción',  'Denominación',
        'Marca', 'Modelo', 'Color', 'Serie', 'Dimensiones', 
        'Estado', 'Observaciones'
    ]
    sheet.append(headers)

    # Obtén los datos del inventario
    inventory = Inventario.objects.all()

    # Agrega los datos al archivo Excel
    for index, item in enumerate(inventory, start=2):  # start=2 para comenzar después de los encabezados
        row = [
            item.id, item.cod_patrimonial, item.cod_interno, item.ano_ingreso, item.denominacion, 
            item.descripcion.descripcion_inventario, item.marca, 
            item.modelo, item.color, item.serie, item.dimensiones, 
            item.estado_mueble.descripcion_estado, item.observaciones
        ]
        sheet.append(row)

    # Guarda el archivo en un objeto BytesIO
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Configura la respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=inventario_Talleres.xlsx'

    return response

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Inventario, pk=pk)
    
    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Actualiza los campos del formulario excepto estado_logico
            product = form.save(commit=False)
            product.estado_logico = True  # Asegúrate de que el estado lógico se mantenga en True
            product.save()
            return redirect('home')
    else:
        form = InventarioForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form})