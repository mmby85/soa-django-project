import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.finance.models import Invoice

from .models import *


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = 'students'


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    # def get_context_data(self, **kwargs):
    #     context = super(StudentDetailView, self).get_context_data(**kwargs)
    #     context["payments"] = Invoice.objects.filter(student=self.object)
    #     return context


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = "__all__"
    success_message = "New student successfully added."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        return form


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['passport'].widget = widgets.FileInput()
        return form


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")


class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/manage/list"
    success_message = "Successfully uploaded students"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "registration_number",
                "surname",
                "firstname",
                "other_names",
                "gender",
                "parent_number",
                "address",
                "current_class",
            ]
        )

        return response


#Manage Module Views

class ModuleListView(LoginRequiredMixin, ListView):
    model = Module
    template_name = "module/module_list.html"
    context_object_name = 'students'

class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = "module/module_detail.html"

class ModuleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Module
    fields = "__all__"
    success_message = "New module successfully added."
    template_name = "module/module_form.html"

class ModuleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Module
    fields = "__all__"
    success_message = "Record successfully updated."


class ModuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Module
    success_url = reverse_lazy("module-list")

#Manage Teacher Views

class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = "teacher/teacher_list.html"
    context_object_name = 'students'

class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = "teacher/teacher_detail.html"

class TeacherCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Teacher
    fields = "__all__"
    success_message = "New teacher successfully added."
    template_name = "teacher/teacher_form.html"

class TeacherUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Teacher
    fields = "__all__"
    success_message = "Record successfully updated."
    template_name = "teacher/teacher_form.html"

class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    success_url = reverse_lazy("teacher-list")
    template_name = "teacher/teacher_confirm_delete.html"


#Manage Session Views
class SessionListView(LoginRequiredMixin, ListView):
    model = Session
    template_name = "session/session_list.html"
    context_object_name = 'students'

class SessionDetailView(LoginRequiredMixin, DetailView):
    model = Session
    template_name = "session/session_detail.html"

class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Session
    fields = "__all__"
    success_message = "New session successfully added."
    template_name = "session/session_form.html"

class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Session
    fields = "__all__"
    success_message = "Record successfully updated."

class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = Session
    success_url = reverse_lazy("session-list")
