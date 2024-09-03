from django.shortcuts import render
import requests
from django.http import HttpResponse
import mimetypes

def index(request):
    return render(request, 'disk_viewer/index.html')

def list_files(request):
    public_key = request.GET.get('public_key')

    if not public_key:
        return render(request, 'disk_viewer/index.html', {'error': 'Public key is required'})

    url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
    response = requests.get(url)

    if response.status_code == 200:
        files = response.json()['_embedded']['items']
        return render(request, 'disk_viewer/files.html', {'files': files})
    else:
        return render(request, 'disk_viewer/index.html', {'error': 'Could not retrieve files'})

def download_file(request, file_path):
    public_key = request.GET.get('public_key')

    download_url = f'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={public_key}&path={file_path}'
    download_response = requests.get(download_url)

    if download_response.status_code == 200:
        href = download_response.json()['href']
        file_response = requests.get(href)

        content_type, _ = mimetypes.guess_type(file_path)
        response = HttpResponse(file_response.content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename={file_path.split("/")[-1]}'
        return response
    else:
        return HttpResponse('Failed to download the file.', status=404)