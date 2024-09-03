from django.urls import path

from disk_viewer import views


urlpatterns = [
    path('', views.index, name='index'),
    path('files/', views.list_files, name='list_files'),
    path('download/<path:file_path>/', views.download_file, name='download_file'),
]
