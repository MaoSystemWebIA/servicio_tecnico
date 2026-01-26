from django.urls import path
from .views import chatbot, diagnostico_inteligente

urlpatterns = [
    path('chatbot/', chatbot, name='chatbot'),
    path('diagnostico/', diagnostico_inteligente, name='diagnostico_inteligente'),
]
