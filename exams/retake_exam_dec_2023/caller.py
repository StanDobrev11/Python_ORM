import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Match, Tournament


# Create queries within functions
def get_tennis_players(search_name=None, search_country=None):
    """
    It retrieves tennis player objects by partially and case-insensitively matching the given searching criteria for
    full name and/or country.
    """
    if not search_name and not search_country:
        return ''

    if search_name and search_country:
        search_query = Q(full_name__icontains=search_name, country__icontains=search_country)
    elif search_name:
        search_query = Q(full_name__icontains=search_name)
    else:
        search_query = Q(country__icontains=search_country)

    results = TennisPlayer.objects.filter(search_query).order_by('ranking')

    if results.count() > 0:
        return '\n'.join(f"Tennis Player: {player.full_name}, "
                         f"country: {player.country},"
                         f" ranking: {player.ranking}" for player in results)
    else:
        return ''


def get_top_tennis_player():
    """It retrieves the tennis player with the greatest number of wins.
    If there is more than one tennis player with the same number of wins, order them by full name,
    ascending, and return the first one’s info.
    If there are no players, return an empty string ("").
    """
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if top_player:
        return f"Top Tennis Player: {top_player.full_name} with {top_player.wins_count} wins."
    else:
        return ''


def get_tennis_player_by_matches_count():
    """It retrieves the tennis player with the greatest number of matches played.
    If there is more than one tennis player with the same number of matches, order them by ranking,
    ascending, and return the first one’s info.
    """
    player = TennisPlayer.objects.annotate(matches_played=Count('matches')).order_by('-matches_played',
                                                                                     'ranking').first()

    if not player or Match.objects.count() == 0:
        return ''

    return f"Tennis Player: {player.full_name} with {player.matches_played} matches played."


def get_tournaments_by_surface_type(surface=None):
    """It retrieves the tournament objects whose surface type matches the given string partially 
    and case-insensitively. Order them by start date, descending. 
    """
    if surface is None or Tournament.objects.count() == 0:
        return ''

    # tournaments = Tournament.objects.prefetch_related('matches') \
    #     .annotate(num_matches=Count('matches')) \
    #     .filter(surface_type__icontains=surface) \
    #     .order_by('-start_date')

    tournaments = (Tournament
                   .objects
                   .filter(surface_type__icontains=surface)
                   .annotate(num_matches=Count('matches'))
                   .order_by('-start_date')
                   )

    if not tournaments.exists():
        return ''

    return '\n'.join(
        f'Tournament: {tournament.name}, '
        f'start date: {tournament.start_date}, '
        f'matches: {tournament.num_matches}'
        for tournament in tournaments
    )


def get_latest_match_info():
    """It retrieves the latest match considering its date played.
    If you have matches with the same date and time, get the last one (last id).
    Players' full names must be separated by " vs " and ordered by full name, ascending.
    If the winner is None, return "TBA" instead of the winner’s full name.
    if there are no matches, return an empty string ("").

    """

    latest_match = Match.objects.select_related('tournament', 'winner').prefetch_related('players').order_by(
        '-date_played', '-id').first()

    if latest_match:
        players = latest_match.players.all().order_by('full_name')
        players_names = ' vs '.join(player.full_name for player in players)

        return (f"Latest match played on: {latest_match.date_played}, "
                f"tournament: {latest_match.tournament.name}, "
                f"score: {latest_match.score}, "
                f"players: {players_names}, "
                f"winner: {latest_match.winner.full_name if latest_match.winner else 'TBA'}, "
                f"summary: {latest_match.summary}")
    else:
        return ''


def get_matches_by_tournament(tournament_name=None):
    """It retrieves all matches by the given tournament name (exact match)
    and orders them by the date played, descending."""

    if not Tournament.objects.exists():
        return "No matches found."

    try:
        tournament = Tournament.objects.get(name=tournament_name)
    except Tournament.DoesNotExist:
        return "No matches found."

    matches = Match.objects.filter(tournament=tournament).select_related('winner').order_by('-date_played')

    if matches.count() == 0:
        return "No matches found."

    return '\n'.join(
        f"Match played on: {match.date_played}, "
        f"score: {match.score}, "
        f"winner: {match.winner.full_name if match.winner else 'TBA'}"
        for match in matches
    )

# if __name__ == '__main__':
#     print(get_tournaments_by_surface_type('Clay'))
