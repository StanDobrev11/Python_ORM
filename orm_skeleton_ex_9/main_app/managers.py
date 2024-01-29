from decimal import Decimal

from django.db import models
from django.db.models import Count, Max, Avg, Min


class RealEstateListingManager(models.Manager):

    def by_property_type(self, property_type: str):
        """
        returns all real estate objects (in a queryset) from the given property type
        """

        return self.get_queryset().filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        """
        returns all real estate objects (in a queryset)  between the given price range (inclusive)
        """

        return self.get_queryset().filter(price__range=[min_price, max_price])

    def with_bedrooms(self, bedrooms_count: int):
        """
        returns all real estate objects (in a queryset)  with the given bedroom count.
        """

        return self.get_queryset().filter(bedrooms=bedrooms_count)

    def popular_locations(self):
        """
        returns the 2 most visited locations, ordered by the id of the location (ascending).
        The most visited locations are those with the most database records
        """

        return self.values('location').annotate(counted=Count('location')).order_by('-counted', 'location')[:2]


class VideoGameManager(models.Manager):

    def games_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        result_queryset = self.aggregate(highest_rating=Max('rating'))

        return self.filter(rating=result_queryset['highest_rating'])

    def lowest_rated_game(self):
        result_queryset = self.aggregate(lowest_rating=Min('rating'))

        return self.filter(rating=result_queryset['lowest_rating'])

    def average_rating(self):
        result = self.aggregate(average_rating=Avg('rating'))

        return f"{result['average_rating'] :.1f}"
