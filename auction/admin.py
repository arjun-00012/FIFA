from django.contrib import admin
from .models import Team, Player

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget', 'captain_name', 'manager_name')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'base_amount', 'current_bid', 'status', 'team')
    list_filter = ('status', 'position', 'team')
    search_fields = ('name',)