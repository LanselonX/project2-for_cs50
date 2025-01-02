from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionList(models.Model):
    CATEGORY_CHOICES = [
        ('art', 'Art'),
        ('electronic', 'Electronic'),
        ('cars', 'Cars'),
    ]
    title = models.CharField(max_length=64, verbose_name="title")
    description = models.TextField(verbose_name="description")
    start_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="start_price")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_list", verbose_name="creator")
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="winner")
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, verbose_name="category")
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.title}: {self.description}: {self.start_price}"

class Lot(models.Model):
    lot_author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="lot_author", verbose_name="lot_author")
    lot_info = models.ForeignKey(AuctionList, on_delete=models.CASCADE, verbose_name="lot_info")
    lot_bid = models.DecimalField(max_digits=10, decimal_places=2)
    lot_done_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["lot_info", "lot_bid"]

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    auction_list = models.ManyToManyField(AuctionList, related_name='watchlist')

    def __str__(self):
        return f"{self.user.username}'s watchlist"

class Commentary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    auc_post = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name='comment_post')
    text = models.TextField(verbose_name="comment")
