from django.urls import path

from .views import *

urlpatterns = [
    path("student/list", StudentListView.as_view(), name="student-list"),
    path("student/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("student/create/", StudentCreateView.as_view(), name="student-create"),
    path("student/<int:pk>/update/", StudentUpdateView.as_view(), name="student-update"),
    path("student/delete/<int:pk>/", StudentDeleteView.as_view(), name="student-delete"),
    path("student/upload/", StudentBulkUploadView.as_view(), name="student-upload"),
    path("student/download-csv/", DownloadCSVViewdownloadcsv.as_view(), name="download-csv"),
    path("module/list", ModuleListView.as_view(), name="module-list"),
    path("module/<int:pk>/", ModuleDetailView.as_view(), name="module-detail"),
    path("module/create/", ModuleCreateView.as_view(), name="module-create"),
    path("module/<int:pk>/update/", ModuleUpdateView.as_view(), name="module-update"),
    path("module/delete/<int:pk>/", ModuleDeleteView.as_view(), name="module-delete"),
    path("teacher/list", TeacherListView.as_view(), name="teacher-list"),
    path("teacher/<int:pk>/", TeacherDetailView.as_view(), name="teacher-detail"),
    path("teacher/create/", TeacherCreateView.as_view(), name="teacher-create"),
    path("teacher/<int:pk>/update/", TeacherUpdateView.as_view(), name="teacher-update"),
    path("teacher/delete/<int:pk>/", TeacherDeleteView.as_view(), name="teacher-delete"),
    path("session/list", SessionListView.as_view(), name="session-list"),
    path("session/<int:pk>/", SessionDetailView.as_view(), name="session-detail"),
    path("session/create/", SessionCreateView.as_view(), name="session-create"),
    path("session/<int:pk>/update/", SessionUpdateView.as_view(), name="session-update"),
    path("session/delete/<int:pk>/", SessionDeleteView.as_view(), name="session-delete"),
    
    ]
