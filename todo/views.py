from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, UserCreateForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
import re
from django.contrib import messages


# Create your views here.
def home(request):
    params = dict()
    if request.user.is_authenticated:
        form = TodoForm()
        todos = Todo.objects.filter(user=request.user, completed_time=None).order_by('-created_time')
        pages = Paginator(todos, 10)
        page_num = request.GET.get('page', 1)
        try:
            page = pages.page(page_num)
        except EmptyPage:
            page = pages.page(1)

        params = {'todos': todos, 'page': page, 'form' : form}
    
    return render(request, 'todo/index.html', params)

def signupuser(request):
    form = UserCreateForm()
    params = {'form': form}
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('todo:home')
            except IntegrityError:
                params['error'] = 'Username already exists. Please use a different username!'

        else:
            params['error'] = 'Passwords did not match.'
            return render(request, 'todo/signup.html', params)
    return render(request, 'todo/signup.html', params)

def loginuser(request):
    form = AuthenticationForm()
    params = {'form': form}
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
       
        if user is None:
            params['error'] = "Username and Passwords Don't match!"
            return render(request, 'todo/login.html', params)
        
        login(request, user)
        url = request.GET.get('next','/')
        return redirect(url)

    return render(request, 'todo/login.html', params)

@login_required
def addtodo(request):
    form = TodoForm()
    params = {'form': form}
    if request.method == "POST":
        formtodo = TodoForm(request.POST)
        try:
            newtodo = formtodo.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
        except ValueError:
            messages.error(request, 'Bad Data Entered' )
        
        url = request.POST.get('url', '/')
        return redirect(url)




@login_required
def search(request):
    if 'query' in request.GET:
        query = request.GET['query']
        or_query = Q(task__icontains=query)
        or_query.add(Q(desc__icontains=query), Q.OR)
        todos = Todo.objects.filter(or_query, user=request.user).order_by('-imp', '-completed_time', '-created_time', )
        pages = Paginator(todos, 10) 
        page_num = request.GET.get('page', '1')
        try:
            page = pages.page(page_num)
        except EmptyPage:
            page = pages.page(1)

        params = {'todos': todos, 'query' : query, 'page':page }
        return render(request, 'todo/search.html', params)

    return render(request, 'todo/search.html', )


@login_required
def allcompletedtodo(request):
    completed_todos = Todo.objects.filter(user=request.user, completed_time__isnull=False).order_by('-completed_time')
    pages = Paginator(completed_todos, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = pages.page(page_num)
    except EmptyPage:
        page = pages.page(1)
    params = {'comps': completed_todos, 'page' : page}

    return render(request, 'todo/allcompletetodo.html', params)

@login_required
def viewtodo(request, tid):

    todo = get_object_or_404(Todo, pk=tid, user=request.user)
    view_url = '/viewtodo/' + str(tid)
    form = TodoForm(instance=todo)
    params = {'todo': todo, 'form' : form,  'view_url' : view_url }
    if request.method == 'GET':
        return render(request, 'todo/viewtodo.html', params)
    try:
        formtodo = TodoForm(request.POST, instance=todo)
        formtodo.save()
    except ValueError:
        form = TodoForm(instance=todo)
        view_url = '/viewtodo/' + str(tid)
        params = {'todo': todo, 'form' : form, 'view_url' : view_url}
        params['error'] = 'Bad Values'
        return render(request, 'todo/viewtodo.html', params)
    
    url = request.POST.get('url', '/')
    return redirect(url)

@login_required
def completetodo(request, tid):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=tid, user=request.user)
        if todo.completed_time:
            todo.completed_time = None
        else:
            todo.completed_time = timezone.now()

        todo.save()
        url = request.POST.get('url', '/')

    return redirect(url)

@login_required
def imptodo(request, tid):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=tid, user=request.user)

        url = request.POST.get('url', '/')

        if todo.imp:
            todo.imp = False
        else:
            todo.imp = True
        todo.save()

    return redirect(url)

@login_required
def deletetodo(request, tid):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=tid, user=request.user)
        todo.delete()
        url = request.POST.get('url', '/')
        if re.search('/viewtodo/',url):
            url = '/'


    return redirect(url)

@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
    return redirect('todo:home')