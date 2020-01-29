from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Subject, List, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import models

def index(request):
    if request.user.is_authenticated:
        latest_subject_list = Subject.objects.order_by('-count')
        context = {'latest_subject_list': latest_subject_list}
        return render(request, 'notes/index.html', context)
    else:
        return render(request, 'notes/login.html')

def detail(request, subject_id):
    if request.user.is_authenticated:
        subject = get_object_or_404(Subject, pk=subject_id)
        return render(request, 'notes/detail.html', {'subject': subject})
    else:
        return HttpResponseRedirect('/')

def detail_add(request, subject_id):
    if request.user.is_authenticated:
        subject = get_object_or_404(Subject, pk=subject_id)
        return render(request, 'notes/detail_add.html', {'subject': subject})
    else:
        return HttpResponseRedirect('/')

def results(request, subject_id):
    if request.user.is_authenticated:
        subject = get_object_or_404(Subject, pk=subject_id)
        subject.count = subject.list_set.count()
        subject.save()
        List.objects.order_by('-due_date')
        return render(request, 'notes/results.html', {'subject': subject})
    else:
        return HttpResponseRedirect('/')

def edit(request, subject_id):
    if request.user.is_authenticated:
        subject = get_object_or_404(Subject, pk=subject_id)
        try:
            selected_list = subject.list_set.get(pk=request.POST['list'])
        except (KeyError, List.DoesNotExist):
            return render(request, 'notes/detail.html', {
                'subject': subject,
                'error_message': "No List Selected",
            })
        else:
            selected_list.completed = True
            selected_list.save()
            if selected_list.completed == True:
                selected_list.delete()
            return HttpResponseRedirect(reverse('notes:results', args=(subject.id,)))
    else:
        return HttpResponseRedirect('/')


def add(request, subject_id):
    if request.user.is_authenticated:
        subject = get_object_or_404(Subject, pk=subject_id)
        if request.method == 'POST':
            add_id = request.POST.get('textfield', None)
            date_id = request.POST.get('datefield', None)
            try:
                s = Subject.objects.get(pk=subject_id)
                error_message = ""
                if(add_id=="" or date_id==""):
                    if(add_id==""):
                        error_message = "No added list"
                    elif(date_id==""):
                        error_message = "No added date"
                    return render(request, 'notes/detail_add.html', {
                    'subject': subject,
                    'error_message': error_message,
                })
                isValidDate = True
                #checks if there is no alphabets
                if(date_id.upper().isupper()):
                    isValidDate = False
                else:
                    #checks if there is 2 /
                    if(not date_id.count('-') == 2):
                        isValidDate = False
                    else:
                        year,month,day = date_id.split('-')
                        try: 
                            datetime.datetime(int(year), int(month), int(day))
                        except ValueError:
                            isValidDate = False
                if(not isValidDate):
                    return render(request, 'notes/detail_add.html', {
                    'subject': subject,
                    'error_message': "Invalid date",
                    })
                else:
                    print("valid date")
            except (KeyError, add_id==""):
                return render(request, 'notes/detail_add.html', {
                    'subject': subject,
                    'error_message': "Add Error",
                })
            else:
                s.list_set.create(list_text=add_id, completed="False", due_date=date_id)
                s.save()
                return HttpResponseRedirect(reverse('notes:results', args=(subject.id,)))
    else:
        return HttpResponseRedirect('/')


def createUser(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    user = models.CustomUser.objects.create_user(username, email, password, first_name = firstName, last_name = lastName)
    user.save()
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def signIn(request):
    return render(request, "notes/signin.html")

def logOut(request):
    logout(request)
    return HttpResponseRedirect('/')