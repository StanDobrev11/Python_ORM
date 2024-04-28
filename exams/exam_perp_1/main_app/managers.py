from django.db.models import Count
from django.db.models.manager import Manager


class CustomProfileManager(Manager):

    def get_regular_customers(self):
        """
        This method retrieves and returns all profile objects with more than two orders.
        Order profiles by number of orders, descending.
        You should count all orders regardless of their status ("Completed" or "Not Completed").
        """
        return (self.get_queryset()
                .annotate(num_orders=Count('orders'))
                .filter(num_orders__gt=2)
                .order_by('-num_orders'))
