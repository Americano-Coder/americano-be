from django.urls import path, include
from .views import save_expense, get_expenses_list, get_expense_detail, get_expenses_list_attributes_without_date, get_expense_detail_attributes_without_date

urlpatterns = [
    path('save_expense', save_expense, name='save_expense'),
    path('expenses/', get_expenses_list, name='expenses-list'),
    path('expenses/<int:pk>/', get_expense_detail, name='expense-detail'),
    path('expenses/attributes/without-date/', get_expenses_list_attributes_without_date, name='expenses-list-attributes-without-date'),
    path('expenses/attributes/without-date/<int:pk>/', get_expense_detail_attributes_without_date, name='expense-detail-attributes-without-date'),
]