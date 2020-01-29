from django.urls import path

from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:subject_id>/', views.detail, name='detail'),
    path('<int:subject_id>/detail_add', views.detail_add, name='detail_add'),
    path('<int:subject_id>/results/', views.results, name='results'),
    path('<int:subject_id>/edit/', views.edit, name='edit'),
    path('<int:subject_id>/add/', views.add, name='add'),
    path('createUser', views.createUser, name='createUser'),
    path('signin', views.signIn, name='signin'),
    path('auth',views.auth, name='auth'),
    path('logout/', views.logOut, name='logout'),
]