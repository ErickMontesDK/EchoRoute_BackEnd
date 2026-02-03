from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import ClientType, Visit, Client
from .serializers import *

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


@api_view(['GET'])
def get_client_types(request):
    client_types = ClientType.objects.all()
    serializer = ClientTypeSerializer(client_types, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def visit_list(request):
    user_id = request.user.id
    print("user: ", user_id)

    if request.method == 'GET':
        visits = Visit.objects.all()
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        request.data['deliverer'] = user_id
        print(request.data)
        serializer = VisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def visit_detail(request, pk):
    
    visit = get_object_or_404(Visit, pk=pk)
    
    if request.method == 'GET':
        serializer = VisitSerializer(visit)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = VisitSerializer(visit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        visit.delete()
        return Response({'message': 'Visit deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def client_list(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print(request.data)
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def client_detail(request, code):
    client = get_object_or_404(Client, code=code)
    
    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        client.delete()
        return Response({'message': 'Client deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
