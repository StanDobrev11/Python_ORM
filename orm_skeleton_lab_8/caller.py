import os
import django
import yfinance as yf


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# from main_app.models import
# Create and check models
# Run and print your queries
# try:
#     data = yf.download('btc-usd', '2024-01-12', '2024-01-16')
# except IndexError as e:
#     print(str(e))
#
# instances = []
# for date, row in data.iterrows():
#     instance = BitCoin(
#         date=date,
#         open=row['Open'],
#         high=row['High'],
#         low=row['Low'],
#         close=row['Close'],
#         volume=row['Volume']
#     )
#     instances.append(instance)
#
# BitCoin.objects.bulk_create(instances)
