from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='teams/logos/', help_text="Upload team logo/poster from system storage")
    budget = models.DecimalField(decimal_places=2, max_digits=12, default=1000.00)
    
    manager_name = models.CharField(max_length=100)
    manager_image = models.ImageField(upload_to='staff/managers/', default='staff/default-avatar.png')
    
    captain_name = models.CharField(max_length=100)
    captain_image = models.ImageField(upload_to='staff/captains/', default='staff/default-avatar.png')

    def __str__(self):
        return self.name

class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('CB', 'Center Back'),
        ('CMF', 'Central Midfielder'),
        ('FWD', 'Forward'),
    ]
    STATUS_CHOICES = [
        ('UNSOLD', 'Unsold'),
        ('BIDDING', 'Bidding'),
        ('SOLD', 'Sold'),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='players/profiles/', help_text="Upload player photo from system storage")
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    base_amount = models.DecimalField(max_digits=12, decimal_places=2, default=20.00)
    current_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNSOLD')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')

    def __str__(self):
        return f"{self.name} ({self.get_position_display()})"