from django.shortcuts import render
from .models import Expense
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import ExpenseSerializer

# Create your views here.
@api_view(["POST"])
@csrf_exempt
def save_expense(request):
    if request.method == "POST":
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(["GET"])
def get_expenses_list(request):
    expenses = Expense.objects.all()
    data = [{'date': expense.date, 'amount': expense.amount, 'category': expense.category} for expense in expenses]
    return Response(data)

@api_view(["GET"])
def get_expense_detail(request, pk):
    try:
        expenses = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response({"error": "Expense not found"}, status=404)
    data = [{'date': expense.date, 'amount': expense.amount, 'category': expense.category} for expense in expenses]
    return Response(data)

@api_view(["GET"])
def get_expenses_list_attributes_without_date(request):
    expenses = Expense.objects.all()
    data = [{'amount': expense.amount, 'category': expense.category} for expense in expenses]
    return Response(data)

@api_view(["GET"])
def get_expense_detail_attributes_without_date(request, pk):
    try:
        expenses = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response({"error": "Expense not found"}, status=404)
    data = [{'amount': expense.amount, 'category': expense.category} for expense in expenses]
    return Response(data)