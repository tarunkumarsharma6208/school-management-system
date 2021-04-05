from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('teacher-register/', views.teacherRegisterView.as_view(), name='teacherRegister'),
    path('student-register/', views.studentRegisterView.as_view(), name="studentRegister"),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),

    path('attendance/', views.studentAttendanceView, name='attendance'),
    path('rating-message/', views.sendRatingMessageView, name='rating-message'),
    path('assignment/', views.sentAssignmentView, name='assignment'),

    path('teacher-profile/', views.teacherProfileView, name='teacherProfile'),
    path('student-profile/', views.studentProfileView, name='studentProfile'),
    path('student-profile-update/', views.studentProfileUpdateView, name='studentProfileUpdate'),
    path('teacher-profile-update/', views.teacherProfileUpdateView, name='teacherProfileUpdate'),

    path('student-profile-data/', views.studentProfileDataView, name="studentProfileData"),

    path('topper-category/', views.topperCategoryView, name='topperCategory'),
    path('topper-category/<slug:category_slug>/',views.topperCategoryView, name='topper_by_category' ),
    # path('topper/<int:id>', views.topperViews, name='topper'),

]