from django.db.models import Manager, Count


class CustomManager(Manager):

    def get_directors_by_movies_count(self):
        """
        This method retrieves and returns all director objects, ordered by the number of movies each director has
        descending, then by their full names ascending.
        """

        return (self.get_queryset()
                .annotate(movies_count=Count('movies'))
                .order_by('-movies_count', 'full_name')
                )
