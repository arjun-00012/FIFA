import json
import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Team, Player

def auction_dashboard(request):
    teams = Team.objects.all()
    players = Player.objects.all()
    active_player = Player.objects.filter(status='BIDDING').first()
    if not active_player:
        active_player = Player.objects.filter(status='UNSOLD').first()
    
    context = {
        'teams': teams,
        'players': players,
        'active_player': active_player
    }
    return render(request, 'index.html', context)


def backup_tournament_data(request):
    all_teams = Team.objects.all()
    all_players = Player.objects.all()
    combined_query_payload = list(all_teams) + list(all_players)
    serialized_json_data = serializers.serialize("json", combined_query_payload, indent=4)
    response = HttpResponse(serialized_json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="SOFTTAC_LEAGUE_MASTER_BACKUP.json"'
    return response


def export_squad_excel(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    sold_players = Player.objects.filter(team=team, status='SOLD').order_by('position')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="SOFTTAC_{team.name.upper()}_SQUAD.csv"'
    
    writer = csv.writer(response)
    writer.writerow([f"SOFTTAC PREMIER LEAGUE — FINAL SQUAD LIST: {team.name.upper()}"])
    writer.writerow([f"Manager: {team.manager_name}", f"Captain: {team.captain_name}", f"Remaining Bank: ${team.budget}"])
    writer.writerow([])
    writer.writerow(['Player Name', 'Tactical Position Role', 'Auction Purchase Price ($)'])
    
    for player in sold_players:
        writer.writerow([player.name, player.get_position_display(), f"${player.current_bid}"])
        
    return response


def management_panel(request):
    if request.method == 'POST':
        action = request.POST.get('form_type')
        
        if action == 'add_team':
            Team.objects.create(
                name=request.POST.get('name'),
                logo=request.FILES.get('logo'),
                budget=float(request.POST.get('budget', 1000.00)),
                manager_name=request.POST.get('manager_name'),
                manager_image=request.FILES.get('manager_image'),
                captain_name=request.POST.get('captain_name'),
                captain_image=request.FILES.get('captain_image')
            )
        elif action == 'edit_team':
            team = get_object_or_404(Team, id=request.POST.get('team_id'))
            team.name = request.POST.get('name')
            if request.FILES.get('logo'): team.logo = request.FILES.get('logo')
            team.budget = float(request.POST.get('budget', team.budget))
            team.manager_name = request.POST.get('manager_name')
            if request.FILES.get('manager_image'): team.manager_image = request.FILES.get('manager_image')
            team.captain_name = request.POST.get('captain_name')
            if request.FILES.get('captain_image'): team.captain_image = request.FILES.get('captain_image')
            team.save()
        elif action == 'delete_team':
            get_object_or_404(Team, id=request.POST.get('team_id')).delete()

        elif action == 'add_player':
            Player.objects.create(
                name=request.POST.get('name'),
                image=request.FILES.get('image'),
                position=request.POST.get('position'),
                base_amount=float(request.POST.get('base_amount', 20.00)),
                current_bid=0.00,
                status='UNSOLD'
            )
        elif action == 'edit_player':
            player = get_object_or_404(Player, id=request.POST.get('player_id'))
            new_status = request.POST.get('status', player.status)
            
            if player.status == 'SOLD' and player.team and new_status != 'SOLD':
                associated_team = player.team
                associated_team.budget = float(associated_team.budget) + float(player.current_bid)
                associated_team.save()
                
                player.team = None
                player.current_bid = 0.00

            player.name = request.POST.get('name')
            if request.FILES.get('image'): player.image = request.FILES.get('image')
            player.position = request.POST.get('position')
            player.base_amount = float(request.POST.get('base_amount', player.base_amount))
            player.status = new_status
            player.save()
            
        elif action == 'delete_player':
            player = get_object_or_404(Player, id=request.POST.get('player_id'))
            if player.team and player.current_bid > 0:
                associated_team = player.team
                associated_team.budget = float(associated_team.budget) + float(player.current_bid)
                associated_team.save()
            player.delete()

        return redirect('management_panel')

    teams = Team.objects.all()
    players = Player.objects.all()
    return render(request, 'management.html', {'teams': teams, 'players': players})


def search_players(request):
    query = request.GET.get('q', '').strip()
    players = Player.objects.filter(name__icontains=query)
    results = []
    for p in players:
        results.append({
            'id': p.id,
            'name': p.name,
            'position': p.position,
            'base_amount': float(p.base_amount),
            'current_bid': float(p.current_bid),
            'status': p.status,
            'image_url': p.image.url if p.image else '',
            'team_name': p.team.name if p.team else None
        })
    return JsonResponse({'players': results})


@csrf_exempt
def submit_final_sale(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        player_id = data.get('player_id')
        team_id = data.get('team_id')
        final_price = float(data.get('final_price', 0))

        player = get_object_or_404(Player, id=player_id)
        team = get_object_or_404(Team, id=team_id)

        if float(team.budget) < final_price:
            return JsonResponse({'success': False, 'error': 'Insufficient team budget!'}, status=400)

        team.budget = float(team.budget) - final_price
        team.save()

        player.team = team
        player.current_bid = final_price
        player.status = 'SOLD'
        player.save()

        return JsonResponse({
            'success': True,
            'team_id': team.id,
            'updated_budget': float(team.budget),
            'player_name': player.name,
            'manager_name': team.manager_name,
            'manager_img': team.manager_image.url if team.manager_image else '',
            'captain_name': team.captain_name,
            'captain_img': team.captain_image.url if team.captain_image else ''
        })
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)