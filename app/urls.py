from django.urls import path
from . import views

urlpatterns = [
    path('',views.student_list,name="student_list"),
    path('add/',views.student_create,name="add_student"),
    path('delete/<int:id>/',views.student_delete,name="delete_student"),
    path('update/<int:id>/',views.student_update,name="update_student"),
    path('update_status/<int:id>/',views.student_update_status,name="update_student_status"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]