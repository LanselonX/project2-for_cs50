from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

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
    path("closed_auction", views.closed_auctions, name="closed_auctions"),
    path("close_auction/<int:auction_id>", views.close_auction, name="close_auction"),
    path("add_commentary/<int:auction_id>", views.add_commentary, name="add_commentary"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
