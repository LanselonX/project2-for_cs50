from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django import forms
from django.contrib import messages

from .models import User, AuctionList, WatchList


def index(request):
    return render(request, "auctions/index.html", {
        "list": AuctionList.objects.all(),
    })

def auction(request, auction_id):
    auc_list = AuctionList.objects.get(id=auction_id)
    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = WatchList.objects.filter(user = request.user, auction_list=auc_list).exists()

    return render(request, 'auctions/auction.html', {
        "auction": auc_list,
        "in_watchlist": in_watchlist,
    })

def add_watchlist(request, auction_id):
    auc_list = get_object_or_404(AuctionList, id=auction_id)
    watchlist, created = WatchList.objects.get_or_create(user=request.user)
    if watchlist.auction_list.filter(id=auction_id).exists():
        watchlist.auction_list.remove(auc_list)
        messages.info(request, "deleted")
    else:
        watchlist.auction_list.add(auc_list)
        messages.success(request, "success")
    return redirect('watchlist')

def watchlist(request): 
    watchlist, created = WatchList.objects.get_or_create(user = request.user)
    context = {
        "all_watchlist": watchlist.auction_list.all()
    }
    return render(request, 'auctions/watchlist.html', context)

class AddListingForm(forms.ModelForm):
    class Meta:
        model = AuctionList
        fields = ['title', 'description', 'start_price']

def add(request):
    if request.method == 'POST':
        form = AddListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddListingForm()
    return render(request, "auctions/add.html", {
        "form": form
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
