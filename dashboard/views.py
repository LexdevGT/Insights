from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import DataFile
import os
from django.conf import settings
from django.contrib import messages
from .services.data_processor import process_data_files
from django.shortcuts import render


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_path = os.path.join(settings.DATA_DIR, uploaded_file.name)

        # Guardar archivo en el directorio `data`
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Registrar archivo en la base de datos
        DataFile.objects.create(
            name=uploaded_file.name,
            file_type=uploaded_file.content_type,
        )

        # Mensaje de éxito
        messages.success(request, f"File '{uploaded_file.name}' has been uploaded successfully!")
        return HttpResponseRedirect('/upload/')

    return render(request, 'dashboard/upload.html')

def file_list(request):
    processed_files = process_data_files()
    return render(request, 'dashboard/file_list.html', {'files': processed_files})


def dashboard(request):
    # Obtener nombres de desarrolladores dinámicamente (puede ser manual por ahora)
    developers = ["Luis Barrera", "Jonay Medina", "Trino Alfonso Fonseca"]  # Datos temporales

    # Retornar estos datos al contexto de la plantilla
    return render(request, 'dashboard/dashboard.html', {'developers': developers})