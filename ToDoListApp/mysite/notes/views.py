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
        try:
            s = Subject.objects.get(pk=subject_id)
            error_message = ""
            if(add_id==""):
                return render(request, 'notes/detail_add.html', {
                'subject': subject,
                'error_message': "No added list",
            })
        except (KeyError, add_id==""):
            return render(request, 'notes/detail_add.html', {
                'subject': subject,
                'error_message': "Add Error",
            })
        else:
            s.list_set.create(list_text=add_id, completed="False")
            s.save()
            return HttpResponseRedirect(reverse('notes:results', args=(subject.id,)))
