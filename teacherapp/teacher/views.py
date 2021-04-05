from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
import ast
import json
from .forms import *
from .models import *
from .decorators import*
from django.db import transaction
from django.views.generic import CreateView


def home(request):
    return render(request, 'home.html')



# =========student profile home============

class studentRegisterView(CreateView):
    model = User
    form_class = studentRegisterForm
    template_name = 'account/studentRegister.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('studentProfileUpdate')


def studentProfileView(request):
    std_data = studentProfile.objects.get(user=request.user)
    

    return render(request, 'student/studentProfile.html', {'std_dat': std_data})

@student_required
def studentProfileUpdateView(request):

    if request.method == 'POST':
        std_inst = studentProfile.objects.get(user=request.user)
        std_form = studentProfileForm(request.POST, instance=std_inst)
        if std_form.is_valid():
            std_form.save()
            messages.success(request, 'Student Profile updated')
        else:
            messages.error(request, 'Please check An Error occurred')
    else:
        std_form = studentProfileForm()
    return render(request, 'student/studentProfileUpdate.html', {'std_form':std_form})


@student_required
def studentProfileDataView(request):
    if request.method == "GET":
        std_data = studentProfile.objects.get(user=request.user)
        try:
            my_attendance = studentAttendance.objects.all().filter(name=std_data).last()
        except studentAttendance.DoesNotExist:
            my_attendance = None
        try:
            my_assignment = sentAssignment.objects.all().filter(name=std_data).last()
        except sentAssignment.DoesNotExist:
            my_assignment = None

        try:
            my_ratings = sendRatingMessage.objects.all().filter(name=std_data).last()
        except sendRatingMessage.DoesNotExist:
            my_ratings = None
        
    context = {
        'my_attendance': my_attendance,
        'my_assignment': my_assignment,
        'my_ratings': my_ratings,
    }
    return render(request, 'student/studentProfileData.html', context)




# =============== teacher profile home ==============

class teacherRegisterView(CreateView):
    model = User
    form_class = teacherRegisterForm
    template_name = 'account/teacherRegister.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teacherProfile')

def teacherProfileView(request):
    tech_data = teacherDetail.objects.get(user=request.user)
    return render(request, 'teacherProfile.html', {'tech_data':tech_data})

@teacher_required
def teacherProfileUpdateView(request):
    if request.method == 'POST':
        std_inst = teacherDetail.objects.get(user=request.user)
        std_form = teacherDetailForm(request.POST , instance=std_inst)
        # print(std_form)
        if std_form.is_valid():
            std_form.save()
    
            messages.success(request, 'Teacher Profile updated')
        else:
            messages.error(request, 'Please check An Error occurred')
    else:
        std_form = teacherDetailForm()

    return render(request, 'teacherProfileUpdate.html', {'std_form':std_form})


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_teacher:
                return redirect('teacherProfileUpdate')
            elif request.user.is_student:
                return redirect('studentProfileUpdate')
            
        else:
            messages.error(request, 'Username or password is incorrect')
    return render(request, 'account/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')



@teacher_required
def studentAttendanceView(request):
    std = studentAttendance.objects.filter(date=datetime.today())
    present_data = studentAttendance.objects.filter(status='present', date=datetime.today()).count()
    absent_data = studentAttendance.objects.filter(status='absent',  date=datetime.today()).count()
    total_student = present_data + absent_data
    student_status = studentProfile.objects.all()
    if request.method == "POST":
        mydata = request.POST
        roll = [roll for roll,status in mydata.items()]
        value = [status for roll,status in mydata.items()]
        print(mydata)
        roll.pop(0)
        value.pop(0)
        roll = [int(i) for i in roll]
        for i in range(len(roll)):
            std_detail = studentProfile.objects.get(admissionNo=roll[i])
            att_obj = studentAttendance.objects.create(name=std_detail, status=value[i])
            att_obj.save()
        messages.success(request, 'Attendance added successfully')
    return render(request, 'attendance.html', {'student_status': student_status,'present_data': present_data,'absent_data': absent_data,'total_student': total_student, 'std':std })


@teacher_required
def sendRatingMessageView(request):
    object = studentProfile.objects.all()
    if request.method == 'POST':
        my_data = ast.literal_eval(request.POST.get('passedJSON'))
        # print('mydata', my_data)
        for key, value in my_data.items():
            if int(value[0]) != 0:
                profile = studentProfile.objects.get(admissionNo=key)
                alldata = sendRatingMessage.objects.create(name=profile, rate=int(value[0]) ,  message=value[1],)
                # print('all data', alldata)
                alldata.save()
        messages.success(request, 'Message and rating sanded successfully')

    return render(request, 'sendRatingMessage.html', {'object': object,})



@teacher_required
def sentAssignmentView(request):
    student_data = studentProfile.objects.all()
    if request.method == "POST":
        name = request.POST.get('myadmissionNo')
        file = request.FILES.getlist('myfiles')
        print(request.POST)
        for i in file:
            profile = studentProfile.objects.get(admissionNo=name)
            sentAssignment.objects.create(name=profile, image=i).save()
    return render(request, 'assignment.html',{'student_data': student_data})


@teacher_required
def topperCategoryView(request, category_slug=None):
    category = None
    all_data = topperCategory.objects.all()
    topper = Topper.objects.all()
    if category_slug:
        category = get_object_or_404(topperCategory, slug=category_slug)
        # print(category)
        topper.filter(topper_std=category)
    return render(request, 'topper.html', {'all_data':all_data, 'category':category, 'topper': topper})

# def topperViews(request, id):
#     topper_data = get_object_or_404(Topper, id=id)
#     return render(request, 'topperDetail.html', {'topper_data':topper_data})