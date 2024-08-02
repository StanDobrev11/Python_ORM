from django.db.models import Manager, Count


class CustomTennisPlayerManager(Manager):

    def get_tennis_players_by_wins_count(self):
        return (self.get_queryset()
                .annotate(wins_count=Count('wins'))
                .order_by('-wins_count', 'full_name')
                )
