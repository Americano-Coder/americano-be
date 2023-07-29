from django.urls import path, include
from .views import save_expense

urlpatterns = [
    path('save_expense', save_expense, name='save_expense'),
]