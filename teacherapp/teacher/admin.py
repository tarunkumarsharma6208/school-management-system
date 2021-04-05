from django.contrib import admin
from .models import *



admin.site.register(User)

@admin.register(sendRatingMessage)
class sendRatingMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'message', 'rate']



@admin.register(studentProfile)
class studentProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'fatherName', 'motherName', 'admissionNo', 'rollNumber', 'mobileNumber']



@admin.register(teacherDetail)
class teacherDetailAdmin(admin.ModelAdmin):
    list_display = ['fullName', 'classTeacher', 'subject', 'reportingTo', 'mobileNumber']


@admin.register(studentAttendance)
class studentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'date']


@admin.register(sentAssignment)
class sentAssignmentAdmin(admin.ModelAdmin):
    list_display = [ 'image', 'date']


@admin.register(topperCategory)
class topperCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Topper)

