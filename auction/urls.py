from django.urls import path
from . import views

urlpatterns = [
    path('', views.auction_dashboard, name='auction_dashboard'),
    
    path('manage/', views.management_panel, name='management_panel'),
    
    path('export/<int:team_id>/', views.export_squad_excel, name='export_squad_excel'),
    
    path('backup-system-database/', views.backup_tournament_data, name='backup_tournament_data'),
    
    path('api/search/', views.search_players, name='search_players'),
    path('api/finalize-sale/', views.submit_final_sale, name='submit_final_sale'),
]