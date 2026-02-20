from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import ClientType, Visit, Client
from .serializers import *
from django.db.models import Q
from rest_framework.exceptions import NotFound, ValidationError, MethodNotAllowed

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['total_count'] = self.page.paginator.count
        response.data['current_page'] = self.page.number
        response.data['page_size'] = self.page.paginator.per_page
        response.data['has_next'] = self.page.has_next()
        response.data['has_previous'] = self.page.has_previous()
        response.data['next'] = self.get_next_link()
        response.data['previous'] = self.get_previous_link()
        return response


@api_view(['GET'])
def get_client_types(request):
    client_types = ClientType.objects.all()
    serializer = ClientTypeSerializer(client_types, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def visit_list(request):
    user_id = request.user.id

    if request.method == 'GET':
        
        visits = Visit.objects.all().filter(is_deleted=False)

        sorting = request.query_params.get('sorting')
        if sorting:
            visits = visits.order_by(sorting)
        else:
            visits = visits.order_by('-id')

        search_term = request.query_params.get('search_term')
        client_type = request.query_params.get('client_type')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        client_municipality = request.query_params.get('municipality')
        client_sector = request.query_params.get('sector')
        client_state = request.query_params.get('state')

        if search_term:
            visits = visits.filter(
                Q(client__code__icontains=search_term) | 
                Q(client__name__icontains=search_term) | 
                Q(client__address__icontains=search_term) |
                Q(client__neighborhood__icontains=search_term) |
                Q(client__market__icontains=search_term) | 
                Q(client__sector__icontains=search_term) | 
                Q(deliverer__first_name__icontains=search_term) | 
                Q(deliverer__last_name__icontains=search_term) 
            )

        if client_type:
            visits = visits.filter(client__client_type__name__iexact=client_type)
        
        if client_municipality:
            visits = visits.filter(client__municipality__icontains=client_municipality)
        
        if client_sector:
            visits = visits.filter(client__sector__icontains=client_sector)

        if client_state:
            visits = visits.filter(client__state__icontains=client_state)

        if date_from:
            visits = visits.filter(visited_at__gte=date_from)
        
        if date_to:
            visits = visits.filter(visited_at__lte=date_to)

        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(visits, request)
        serializer = VisitSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        request.data['deliverer'] = user_id
        serializer = VisitSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)


@api_view(['GET', 'PATCH', 'DELETE'])
def visit_detail(request, pk):
    
    try:
        visit = Visit.objects.get(pk=pk, is_deleted=False)
    except Visit.DoesNotExist:
        raise NotFound("Visit not found")
    
    if request.method == 'GET':
        serializer = VisitSerializer(visit)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        serializer = VisitSerializer(visit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        raise ValidationError(serializer.errors)
    
    elif request.method == 'DELETE':
        visit.is_deleted = True
        visit.save()
        return Response({'message': 'Visit marked as deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    raise MethodNotAllowed(request.method)


@api_view(['GET', 'POST'])
def client_list(request):
    print("client_list")
    if request.method == 'GET':
        clients = Client.objects.all().filter(is_deleted=False)
        
        code = request.query_params.get('code')
        if code:
            clients = clients.filter(code__icontains=code)
            
        name = request.query_params.get('name')
        if name:
            clients = clients.filter(name__icontains=name)
            
        address = request.query_params.get('address')
        if address:
            clients = clients.filter(address__icontains=address)

        neighborhood = request.query_params.get('neighborhood')
        if neighborhood:
            clients = clients.filter(neighborhood__icontains=neighborhood)

        municipality = request.query_params.get('municipality')
        if municipality:
            clients = clients.filter(municipality__icontains=municipality)

        state = request.query_params.get('state')
        if state:
            clients = clients.filter(state__icontains=state)
            
        market = request.query_params.get('market')
        if market:
            clients = clients.filter(market__icontains=market)
            
        sector = request.query_params.get('sector')
        if sector:
            clients = clients.filter(sector__icontains=sector)
            
        client_type = request.query_params.get('client_type')
        if client_type:
            clients = clients.filter(client_type__name__iexact=client_type)

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
    # Only get clients that are NOT marked as deleted
    client = get_object_or_404(Client, code=code, is_deleted=False)
    
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
        # Perform soft delete
        client.is_deleted = True
        client.save()
        return Response({'message': 'Client marked as deleted'}, status=status.HTTP_204_NO_CONTENT)
