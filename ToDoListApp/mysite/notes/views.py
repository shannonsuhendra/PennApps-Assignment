from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Subject, List
from django.views import generic
import datetime

class IndexView(generic.ListView):
    template_name = 'notes/index.html'
    context_object_name = 'latest_subject_list'

    def get_queryset(self):
        return Subject.objects.order_by('-count')

class DetailView(generic.DetailView):
    model = Subject
    template_name = 'notes/detail.html'

class DetailAddView(generic.DetailView):
    model = Subject
    template_name = 'notes/detail_add.html'

def results(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    subject.count = subject.list_set.count()
    subject.save()
    List.objects.order_by('-due_date')
    return render(request, 'notes/results.html', {'subject': subject})

def edit(request, subject_id):
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

def add(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        add_id = request.POST.get('textfield', None)
        date_id = request.POST.get('datefield', None)
        #month,day,year = date_id.split('/')
        #isValidDate = True
        print(date_id)
        print(add_id)
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
