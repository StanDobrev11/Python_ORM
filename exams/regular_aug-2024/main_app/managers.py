from django.db.models import Manager, Count


class CustomAstronautManager(Manager):

    def get_astronauts_by_missions_count(self):
        return (self.get_queryset()
                .annotate(missions_count=Count('missions'))
                .order_by('-missions_count', 'phone_number')
                )
