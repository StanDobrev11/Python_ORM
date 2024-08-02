import random
from datetime import datetime, timedelta
import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer, Tournament, Match

if __name__ == '__main__':
    # Clear existing data
    Match.objects.all().delete()
    Tournament.objects.all().delete()
    TennisPlayer.objects.all().delete()

    # Create TennisPlayers
    player_names = [
        "Roger Federer", "Rafael Nadal", "Novak Djokovic",
        "Andy Murray", "Stan Wawrinka", "Juan Martin del Potro",
        "Marin Cilic", "David Ferrer", "Kei Nishikori",
        "Dominic Thiem", "Alexander Zverev", "Daniil Medvedev",
        "Stefanos Tsitsipas", "Nick Kyrgios", "Grigor Dimitrov"
    ]

    players = []
    for i, name in enumerate(player_names):
        birth_year = random.randint(1980, 2000)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Ensure valid day of the month
        birth_date = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"

        player = TennisPlayer.objects.create(
            full_name=name,
            birth_date=birth_date,
            country=f"Country {i + 1}",
            ranking=i + 1,
            is_active=bool(random.getrandbits(1))
        )
        players.append(player)

    # Create Tournaments
    tournament_names = [
        "Wimbledon", "French Open", "Australian Open", "US Open",
        "Monte Carlo Masters", "Madrid Open", "Italian Open",
        "Cincinnati Masters", "Shanghai Masters", "Paris Masters"
    ]

    tournaments = []
    for name in tournament_names:
        tournament = Tournament.objects.create(
            name=name,
            location=f"City {random.randint(1, 20)}",
            prize_money=random.uniform(2000000, 50000000),
            start_date=f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            surface_type=random.choice(["Clay", "Grass", "Hard Court"])
        )
        tournaments.append(tournament)

    # Create Matches
    for tournament in tournaments:
        for _ in range(random.randint(5, 15)):
            players_sample = random.sample(players, 2)
            match = Match.objects.create(
                score=f"{random.randint(0, 7)}-{random.randint(0, 7)}, {random.randint(0, 7)}-{random.randint(0, 7)}, {random.randint(0, 7)}-{random.randint(0, 7)}",
                summary=f"A thrilling match between {players_sample[0].full_name} and {players_sample[1].full_name}.",
                date_played=datetime.now() - timedelta(days=random.randint(0, 365)),
                tournament=tournament,
                winner=random.choice(players_sample)
            )
            match.players.set(players_sample)

    print("Sample data created successfully.")