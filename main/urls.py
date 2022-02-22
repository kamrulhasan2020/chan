from django.urls import path
from .import views


app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('board/<str:board>/', views.BoardView.as_view(), name='board'),
    path('post/<str:board>/<str:no>/', views.PostView.as_view(), name='post'),
]