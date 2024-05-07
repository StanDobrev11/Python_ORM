from django.db.models import Manager, Count


class CustomAuthorManager(Manager):

    def get_authors_by_article_count(self):
        return (self.get_queryset()
                .annotate(articles_num=Count('articles'))
                .order_by('-articles_num', 'email')
                )
