from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.db import transaction



class teacherRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        student = teacherDetail.objects.create(user=user)
        student.save()
        return user
        
        

class studentRegisterForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):

        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        teacher = studentProfile.objects.create(user=user)
        teacher.save()
        return user



class studentAttendanceForm(forms.ModelForm):
    class Meta:
        model = studentAttendance
        fields = [  'status',]



class studentProfileForm(forms.ModelForm):
    admissionNo = forms.IntegerField(required = True)
    name = forms.CharField(required = True)
    class Meta:
        model = studentProfile
        fields = ['name', 'fatherName', 'motherName', 'admissionNo', 'rollNumber', 'address', 'mobileNumber']
        exclude = ['user']


class teacherDetailForm(forms.ModelForm):
    class Meta:
        model = teacherDetail
        fields = "__all__"
        exclude = ['user']