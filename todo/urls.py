from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('allcompletedtodo/', views.allcompletedtodo, name='allcompletedtodo'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('addtodo/', views.addtodo, name='addtodo'),
    path('search/', views.search, name='search'),
    path('viewtodo/<int:tid>', views.viewtodo, name='viewtodo'),
    path('completetodo/<int:tid>/complete', views.completetodo, name='completetodo'),
    path('deletetodo/<int:tid>/delete', views.deletetodo, name='deletetodo'),
    path('imptodo/<int:tid>/imp', views.imptodo, name='imptodo'),


]