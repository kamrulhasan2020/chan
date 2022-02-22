from django.urls import path
from .import views


urlpatterns = [
    path('comments/<str:board>/<str:no>/', views.CommentList.as_view(), name='comments'),
    path('comments/<str:board>/<str:no>/<str:parent>/', views.CommentList.as_view(), name='comments'),
]