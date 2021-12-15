from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import StudentClass

#State Class (Absence)
class State(models.Model):
    date = models.DateField()
    motif = models.TextField(max_length=400,blank=True)
    justif = models.FileField(max_length=400,blank=True, upload_to='students/justif')

class Student(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )
    registration_number = models.CharField(max_length=200, unique=True)
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_of_admission = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="students/passports/")
    state = models.ManyToManyField(State, blank=True, null=True)
    email =  models.EmailField(max_length=200)

    class Meta:
        ordering = ["surname", "firstname", "other_name"]

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name} ({self.registration_number})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")

#Group Class
class Group(models.Model):
    name =  models.CharField(max_length=200)
    nb_student = models.IntegerField()
    group_mail =  models.EmailField(max_length=200)
    level= models.CharField(max_length=200)
    students = models.ManyToManyField(Student)
    teachers = models.ManyToManyField('Teacher')


#Session Class
class Session(models.Model):
    h_start = models.TimeField()
    h_end = models.TimeField()
    is_online = models.BooleanField(default=False)
    room_number = models.IntegerField(blank=True)
    goal = models.TextField(max_length=400)
    synopsis = models.TextField(max_length=400)
    logistics = models.TextField(max_length=400, blank=True)
    type_fields = [('regular', 'Regular'), ('remedial','Remedial'),('support','Support'),('training','Training')]
    gender = models.CharField(max_length=60, choices=type_fields)
    records = models.ManyToManyField('Records')

#Module Class
class Module(models.Model):
    name =  models.CharField(max_length=200)
    sessions = models.ManyToManyField(Session)
    supervisor = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    group = models.ManyToManyField(Group)

#Teachers Class
class Teacher(models.Model):
    name =  models.CharField(max_length=200)
    first_name  =  models.CharField(max_length=200)
    prof_mail =  models.EmailField(max_length=200)
    perso_mail =  models.EmailField(max_length=200)
    due = models.IntegerField()
    picture = models.ImageField(upload_to='files/teachers/img')
    modules = models.ManyToManyField(Module)


#Assign class
class Assign(models.Model):
    title = models.CharField(max_length=200)
    date_launch = models.DateField()
    date_due = models.DateField()
    nature = models.CharField(max_length=200)
    desc = models.TextField(max_length=400)
    assign_doc = blank = True
    assign_sub = models.FileField(upload_to='files/assign/submission')
    
    state_fields = [('valid','Valid'),('NotValid','Not Valid')]
    state = models.TextField(max_length = 60, choices = state_fields)
    eva_grade = models.FloatField()
    eva_comm = models.CharField(max_length=200)

#Module Class
class Records(models.Model):
    name =  models.CharField(max_length=200, unique=True)
    url = models.URLField(blank=True)
    content = models.TextField(max_length=600)
    
    type_fields = [('valid','Valid'),('NotValid','Not Valid')]
    type = models.TextField(max_length = 60, choices = type_fields)
    group = models.ManyToManyField(Group)





