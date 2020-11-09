from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('mytodo/', views.mytodo, name='mytodo'),
    path('alltodo/', views.alltodo, name='alltodo'),
    path('allcompletedtodo/', views.allcompletedtodo, name='allcompletedtodo'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('addtodo/', views.addtodo, name='addtodo'),
    path('viewtodo/<int:tid>', views.viewtodo, name='viewtodo'),
    path('completetodo/<int:tid>/complete', views.completetodo, name='completetodo'),
    path('deletetodo/<int:tid>/delete', views.deletetodo, name='deletetodo'),


]