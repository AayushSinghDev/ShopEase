from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('send/', views.chat_send, name='send'),
    path('logs/', views.chat_logs, name='logs'),
]
