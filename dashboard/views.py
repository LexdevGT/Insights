from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import DataFile
from .services.data_processor import (
    process_data_files,
    get_developers,
    get_filtered_chart_data,
    get_time_filters
)
from .services.ai_processor import get_ai_response
import os

@require_http_methods(["GET"])
def ask_ai(request):
    question = request.GET.get('question', '')
    if not question:
        return JsonResponse({'error': 'No question provided'}, status=400)
    return JsonResponse(get_ai_response(question))
def dashboard(request):
    context = {
        "developers": get_developers(),
        "time_filters": get_time_filters(),
    }
    return render(request, "dashboard/dashboard.html", context)

@require_http_methods(["GET"])
def chart_data(request):
    try:
        year = request.GET.get('year', 'all')
        quarter = request.GET.get('quarter', 'all')
        month = request.GET.get('month', 'all')
        developer = request.GET.get('developer', 'all')

        data = get_filtered_chart_data(year, quarter, month, developer)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'data': [],
            'layout': {'title': 'Error loading data'}
        }, status=500)


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        if not uploaded_file.name.endswith(('.xlsx', '.csv')):
            messages.error(request, "Only Excel and CSV files are allowed.")
            return HttpResponseRedirect('/upload/')

        try:
            file_path = os.path.join(settings.DATA_DIR, uploaded_file.name)
            os.makedirs(settings.DATA_DIR, exist_ok=True)

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            DataFile.objects.create(
                name=uploaded_file.name,
                file_type=uploaded_file.content_type,
            )
            messages.success(request, f"File '{uploaded_file.name}' uploaded successfully!")
        except Exception as e:
            messages.error(request, f"Error uploading file: {str(e)}")

        return HttpResponseRedirect('/upload/')
    return render(request, 'dashboard/upload.html')


def file_list(request):
    try:
        files = process_data_files()
        return render(request, 'dashboard/file_list.html', {'files': files})
    except Exception as e:
        messages.error(request, f"Error processing files: {str(e)}")
        return render(request, 'dashboard/file_list.html', {'files': []})
