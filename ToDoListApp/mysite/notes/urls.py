from django.urls import path

from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/detail_add', views.DetailAddView.as_view(), name='detail_add'),
    path('<int:subject_id>/results/', views.results, name='results'),
    path('<int:subject_id>/edit/', views.edit, name='edit'),
    path('<int:subject_id>/add/', views.add, name='add'),
]