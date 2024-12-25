from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib import messages

from .models import User, AuctionList, WatchList, Lot


def index(request):
    active_auctions = AuctionList.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "list": active_auctions,
    })

def closed_auctions(request):
    check_auctions = AuctionList.objects.filter(is_active=False)
    return render(request, 'auctions/closed_auction.html', {
        "list": check_auctions,
    })

def auction(request, auction_id):
    auc_list = AuctionList.objects.get(id=auction_id)
    in_watchlist = False
    maximum_bid = Lot.objects.filter(lot_info=auc_list).order_by('-lot_bid').first()
    if request.user.is_authenticated:
        in_watchlist = WatchList.objects.filter(user = request.user, auction_list=auc_list).exists()
    is_winner = False
    if not auc_list.is_active and auc_list.winner == request.user:
        is_winner = True

    return render(request, 'auctions/auction.html', {
        "auction": auc_list,
        "in_watchlist": in_watchlist,
        "maximum_bid": maximum_bid.lot_bid if maximum_bid else None,
        "bidForm": AddLotForm(),
        "is_winner": is_winner,
    })

def add_watchlist(request, auction_id):
    auc_list = AuctionList.objects.get(id=auction_id)
    user_watchlist, created = WatchList.objects.get_or_create(user=request.user)
    if user_watchlist.auction_list.filter(id=auction_id).exists():
        user_watchlist.auction_list.remove(auc_list)
        messages.info(request, "deleted")
    else:
        user_watchlist.auction_list.add(auc_list)
        messages.success(request, "success")
    return redirect('watchlist')

def watchlist(request):
    user_watchlist, created = WatchList.objects.get_or_create(user = request.user)
    active_watchlist = user_watchlist.auction_list.filter(is_active=True)
    context = {
        "all_watchlist": active_watchlist
    }
    return render(request, 'auctions/watchlist.html', context)

class AddListingForm(forms.ModelForm):
    class Meta:
        model = AuctionList
        fields = ['title', 'description', 'start_price']

class AddLotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = ['lot_bid']
        labels = {
            'lot_bid': 'Choose your maximum bid',
        }

# class CloseAuctionForm(forms.Form):
#     confirm = forms.BooleanField(label="confirm auction closure")
class CloseAuctionForm(forms.ModelForm):
    class Meta:
        model = AuctionList
        fields = ['is_active']

def close_auction(request, auction_id):
    listing = get_object_or_404(AuctionList, id=auction_id)
    if listing.creator != request.user:
        return HttpResponseForbidden("You are not autor")
    if not listing.is_active:
        return redirect('index')

    if request.method == "POST":
        form = CloseAuctionForm(request.POST)
        if form.is_valid():
            highest_bid = Lot.objects.filter(lot_info=listing).order_by('-lot_bid').first()
            if highest_bid:
                listing.winner = highest_bid.lot_author
            listing.is_active = False
            listing.save()
            return redirect('closed_auctions')
    else:
        form = CloseAuctionForm()
    return render(request, 'auctions/closed_auction.html', {
        "listing": listing,
        "form": form,
    })

def lot_bid(request, auction_id):
    listing = get_object_or_404(AuctionList, id=auction_id)

    if request.method == 'POST':
        form = AddLotForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data.get('lot_bid')
            if bid <= 0:
                messages.error(request, "Input an amount greater than 0")
            else:
                maximum_bid = Lot.objects.filter(lot_info=listing).order_by('-lot_bid').first()

                if maximum_bid and bid <= maximum_bid.lot_bid:
                    messages.error(request, "Amount is too low, check the current highest bid")
                else:
                    new_bid = Lot(
                        lot_info=listing,
                        lot_author=request.user,
                        lot_bid=bid
                    )
                    new_bid.save()

                    listing.current_bid = bid
                    listing.save()

                    messages.success(request, "Your bid is currently the highest")
                    return HttpResponseRedirect(reverse('auction', args=[auction_id]))
        else:
            messages.error(request, "Invalid bid form")
    else:
        form = AddLotForm()

    maximum_bid = Lot.objects.filter(lot_info=listing).order_by('-lot_bid').first()
    in_watchlist = WatchList.objects.filter(user=request.user,auction_list=listing).exists() if request.user.is_authenticated else False

    return render(request, 'auctions/auction.html', {
        "auction": listing,
        "bidForm": form,
        "maximum_bid": maximum_bid.lot_bid if maximum_bid else None,
        "in_watchlist": in_watchlist,
    })

def add(request):
    if request.method == 'POST':
        form = AddListingForm(request.POST)
        if form.is_valid():
            auction_save = form.save(commit=False)
            auction_save.creator = request.user
            auction_save.save()
            return redirect('index')
    else:
        form = AddListingForm()
    return render(request, 'auctions/add.html', {'form': form})

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
