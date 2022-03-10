from django.urls import path
from project1 import views


app_name = 'project1'

urlpatterns=[
    path('', views.project2, name='project2'),
    path('project3/<str:pk>/', views.project3, name='project3'),
    path('create-project/',views.createproject, name='create-project'),
    path('update-project/<str:pk>/',views.updateproject, name='update-project'),
    path('delete-project/<str:pk>/',views.deleteproject, name='delete-project')
]