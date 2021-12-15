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
    session = models.ForeignKey('Session', on_delete=models.CASCADE)

    def __str__(self):
        return f"Absence {self.id}"

    def get_absolute_url(self):
        return reverse("state-detail", kwargs={"pk": self.pk})

class Student(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )
    registration_number = models.CharField(max_length=200, unique=True)
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        'Group', on_delete=models.SET_NULL, blank=True, null=True
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
    photo = models.ImageField(blank=True, upload_to="students/photos/")
    state = models.ManyToManyField(State, null=True , blank=True)
    email =  models.EmailField(max_length=200)
    
    state_list = [('present','Present'),('absent','Absent'),('late','Late'),('excluded','Excluded')]
    situation_list = [('new', 'New'), ('repeating','Repeating') , ('derogatory','Derogatory') , ('other','Other')]

    state_choice = models.CharField(max_length=20, choices=state_list, blank=True)
    situation = models.CharField(max_length=20, choices=situation_list, blank=True)

    class Meta:
        ordering = ["surname", "firstname"]

    def __str__(self):
        return f"{self.surname} {self.firstname} ({self.registration_number})"

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
    students = models.ManyToManyField(Student, blank=True)
    teachers = models.ManyToManyField('Teacher', blank=True)
    
    def __str__(self):
        return f"Group {self.name}"

    def get_absolute_url(self):
        return reverse("group-detail", kwargs={"pk": self.pk})

#Session Class
class Session(models.Model):
    h_start = models.TimeField(verbose_name="Starting Time")
    h_end = models.TimeField(verbose_name="Ending Time")
    is_online = models.BooleanField(default=False)
    room_number = models.IntegerField(blank=True, null=True)
    goal = models.TextField(max_length=400)
    synopsis = models.TextField(max_length=400)
    logistics = models.TextField(max_length=400, blank=True)
    type_fields = [('regular', 'Regular'), ('remedial','Remedial'),('support','Support'),('training','Training')]
    gender = models.CharField(verbose_name="Type",max_length=60, choices=type_fields)
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Session {self.id}"

    def get_absolute_url(self):
        return reverse("session-detail", kwargs={"pk": self.pk})

#Module Class
class Module(models.Model):
    name =  models.CharField(max_length=200)
    supervisor = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    group = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return f"module {self.name}"

    def get_absolute_url(self):
        return reverse("module-detail", kwargs={"pk": self.pk})

#Teachers Class
class Teacher(models.Model):
    name =  models.CharField(max_length=200)
    first_name  =  models.CharField(max_length=200)
    prof_mail =  models.EmailField(max_length=200)
    perso_mail =  models.EmailField(max_length=200)
    due = models.IntegerField()
    picture = models.ImageField(upload_to='files/teachers/img')
    modules = models.ManyToManyField(Module, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.name}"

    def get_absolute_url(self):
        return reverse("teacher-detail", kwargs={"pk": self.pk})

#Assign class
class Assign(models.Model):
    title = models.CharField(max_length=200)
    date_launch = models.DateField()
    date_due = models.DateField()
    nature = models.CharField(max_length=200)
    desc = models.TextField(max_length=400)
    assign_doc = models.FileField(upload_to='files/assign/assignment', blank = True)
    assign_sub = models.FileField(upload_to='files/assign/submission')
    
    state_fields = [('valid','Valid'),('NotValid','Not Valid')]
    state = models.TextField(max_length = 60, choices = state_fields)
    eva_grade = models.FloatField()
    eva_comm = models.CharField(max_length=200)
    group = models.ManyToManyField(Student, blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title} {self.id}"

    def get_absolute_url(self):
        return reverse("assign-detail", kwargs={"pk": self.pk})

#Records Class
class Records(models.Model):
    name =  models.CharField(max_length=200, unique=True)
    url = models.URLField(blank=True)
    content = models.TextField(max_length=600)
    
    type_fields = [('valid','Valid'),('NotValid','Not Valid')]
    type = models.TextField(max_length = 60, choices = type_fields)
    group = models.ManyToManyField(Group, blank=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.id}"

    def get_absolute_url(self):
        return reverse("record-detail", kwargs={"pk": self.pk})



