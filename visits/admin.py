from django.contrib import admin
from .models import ClientType, Client, Visit, Route


class ClientTypeAdmin(admin.ModelAdmin):
    list_display = ("id",'name', 'abbreviation')

class ClientAdmin(admin.ModelAdmin):
    list_display = ("id",'code', 'name', 'client_type', 'address', 'neighborhood', 'municipality', 'state', 'latitude', 'longitude', 'sector', 'market')

class VisitAdmin(admin.ModelAdmin):
    list_display = ("id",'client', 'deliverer', 'visited_at', 'latitude_recorded', 'longitude_recorded', 'is_productive', 'is_valid', 'distance_from_client', 'notes')

class RouteAdmin(admin.ModelAdmin):
    list_display = ("id",'name', 'deliverer', 'day_of_week')

admin.site.register(ClientType, ClientTypeAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Route, RouteAdmin)