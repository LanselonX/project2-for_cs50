from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:auction_id>", views.auction, name="auction"),
    path("add_watchlist/<int:auction_id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add", views.add, name="add"),
    path("lot/<int:auction_id>", views.lot_bid, name="lot_bid"),
]
