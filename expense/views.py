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