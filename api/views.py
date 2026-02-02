from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import ClientType, Visit
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, ClientTypeSerializer, VisitSerializer

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
    if request.method == 'GET':
        visits = Visit.objects.all()
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
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
