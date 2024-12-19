from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionList(models.Model):
    title = models.CharField(max_length=64, verbose_name="title")
    description = models.TextField(verbose_name="description")
    start_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="start_price")

    def __str__(self):
        return f"{self.title}: {self.description}: {self.start_price}"
    

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    auction_list = models.ManyToManyField(AuctionList, related_name='watchlist')

    def __str__(self):
        return f"{self.user.username}'s watchlist"