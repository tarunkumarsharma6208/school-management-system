from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.urls import reverse



class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class studentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    fatherName = models.CharField(max_length=100, null=True, blank=True)
    motherName = models.CharField(max_length=100, null=True, blank=True)
    admissionNo = models.IntegerField(null=True, blank=True, unique=True)
    rollNumber = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    mobileNumber = models.CharField(max_length=10, blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)
        
class teacherDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fullName = models.CharField(max_length=100, null=True, blank=True)
    classTeacher = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    reportingTo = models.CharField(max_length=100, null=True, blank=True)
    mobileNumber = models.CharField(max_length=10, blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.user.username)

class sendRatingMessage(models.Model):
    RATE_CHOICES = (
        
        (0, 'zero'),
        (1, 'one'),
        (2, 'two'),
        (3, 'three'),
        (4, 'four'),
        (5, 'five'),
    )
    name = models.ForeignKey(studentProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=300, null=True, blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class studentAttendance(models.Model):
    CHOICES = (
        ('present', 'present'),
        ('absent', 'absent'),
    )
    name = models.ForeignKey(studentProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=CHOICES)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Student Attendance'

    def __str__(self):
        return str(self.name)


class sentAssignment(models.Model):
    name = models.ForeignKey(studentProfile, on_delete=models.CASCADE)
    image = models.FileField(upload_to='assignment/')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image)


class topperCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse('topper_by_category', args=[self.slug])

    def __str__(self):
        return str(self.name)


class Topper(models.Model):
    student = models.ForeignKey(studentProfile, on_delete=models.CASCADE)
    teacher = models.ForeignKey(teacherDetail, on_delete=models.CASCADE)
    topper_std = ForeignKey(topperCategory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.topper_std)

    

