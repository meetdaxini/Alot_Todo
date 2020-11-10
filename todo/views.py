from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, UserCreateForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def home(request):
    params = dict()
    if request.user.is_authenticated:
        get_todos = Todo.objects.filter(user=request.user, completed_time=None).order_by('-created_time')
        todo_count = len(get_todos)
        # print(todo_count)
        todos = get_todos[:5]
        get_completedtodos = Todo.objects.filter(user=request.user, completed_time__isnull=False).order_by('-completed_time')
        completedtodo_count = len(get_completedtodos)
        # print(completedtodos_count)
        completedtodos = get_completedtodos[:5]
        params = {'todos': todos, 'comps' : completedtodos, 'todo_count': todo_count, 'completedtodo_count' : completedtodo_count }

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
                return redirect('todo:mytodo')
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
            params['error'] = "Username and Passwords Don't macth!"
            return render(request, 'todo/login.html', params)
        
        login(request, user)
        return redirect('todo:mytodo')

    return render(request, 'todo/login.html', params)

@login_required
def addtodo(request):
    form = TodoForm()
    params = {'form': form}
    if request.method == "POST":
        formtodo = TodoForm(request.POST)
        newtodo = formtodo.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        return redirect('todo:mytodo')

    return render(request, 'todo/addtodo.html', params)

@login_required
def mytodo(request):
    get_todos = Todo.objects.filter(user=request.user, completed_time=None).order_by('-created_time')
    todo_count = len(get_todos)
    # print(todo_count)
    todos = get_todos[:5]
    get_completedtodos = Todo.objects.filter(user=request.user, completed_time__isnull=False).order_by('-completed_time')
    completedtodo_count = len(get_completedtodos)
    # print(completedtodos_count)
    completedtodos = get_completedtodos[:5]
    params = {'todos': todos, 'comps' : completedtodos, 'todo_count': todo_count, 'completedtodo_count' : completedtodo_count }
    return render(request, 'todo/mytodo.html', params)

@login_required
def alltodo(request):
    todos = Todo.objects.filter(user=request.user, completed_time=None).order_by('-created_time')
    todo_count = len(todos)
    pages = Paginator(todos, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = pages.page(page_num)
    except EmptyPage:
        page = pages.page(1)
    params = {'todos': todos, 'todo_count': todo_count, 'page' : page}
    return render(request, 'todo/alltodo.html', params)

@login_required
def allcompletedtodo(request):
    completed_todos = Todo.objects.filter(user=request.user, completed_time__isnull=False).order_by('-completed_time')
    completedtodo_count = len(completed_todos)
    pages = Paginator(completed_todos, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = pages.page(page_num)
    except EmptyPage:
        page = pages.page(1)
    params = {'comps': completed_todos, 'comp_count' : completedtodo_count, 'page' : page}

    return render(request, 'todo/allcompletetodo.html', params)

@login_required
def viewtodo(request, tid):

    todo = get_object_or_404(Todo, pk=tid, user=request.user)
    form = TodoForm(instance=todo)
    params = {'todo': todo, 'form' : form }
    if request.method == 'GET':
        return render(request, 'todo/viewtodo.html', params)
    try:
        formtodo = TodoForm(request.POST, instance=todo)
        formtodo.save()
    except ValueError:
        form = TodoForm(instance=todo)
        params = {'todo': todo, 'form' : form }
        params['error'] = 'Bad Values'
        return render(request, 'todo/viewtodo.html', params)

    return redirect('todo:mytodo')

@login_required
def completetodo(request, tid):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=tid, user=request.user)
        todo.completed_time = timezone.now()
        todo.save()
    return redirect('todo:mytodo')

@login_required
def deletetodo(request, tid):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=tid, user=request.user)
        todo.delete()
    return redirect('todo:mytodo')


def logoutuser(request):
    if request.method == "POST":
        logout(request)
    return redirect('todo:home')