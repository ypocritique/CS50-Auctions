
from msilib.schema import Error
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.template.defaultfilters import slugify
from django.contrib import messages
from .models import *
from auctions.forms import ListingForm, BidForm, CommentForm



def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all().order_by('-created_on')
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


''' ↓↓↓↓↓↓↓↓↓↓↓↓↓↓☻ AUCTION VIEW CONTROLLER ☻↓↓↓↓↓↓↓↓↓↓↓↓↓ '''

""" ============== CREATE A LISTING ================ """
@login_required
def create(request):
    # Check if method of form is post
    if request.method == "POST":
        
        form = ListingForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.slug = slugify(listing.title)
            listing.price = listing.price
            listing.save()

            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "auctions/create.html", {
                'form' : form
                })
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm()
        })


""" ===============WATCHING PART================ """
@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "watchlist": Listing.objects.filter(watching=request.user).order_by('-created_on')
    })

""" ↓↓↓ Add and Remove listing from Watchlist ↓↓↓ """
@login_required
def watch_edition (request, listing_slug):

    try:
        listing = Listing.objects.get(slug=listing_slug)

        if request.user in listing.watching.all():
            listing.watching.remove(request.user)
            
        else:
            listing.watching.add(request.user)

        return HttpResponseRedirect(reverse('watchlist'))
    except:
        print("Closed listing")
        
    return HttpResponseRedirect(reverse('watchlist'))


    


""" ===============LISTING VIEW PART================ """
def listing(request, listing_slug):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    #listing = Listing.objects.get(slug=listing_slug)
    listing = get_object_or_404(Listing, slug=listing_slug)
    price = int(listing.price )

    if request.user in listing.watching.all():
        listing.is_watched = True
    else:
        listing.is_watched = False

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'title': listing.title,
        'image': listing.image,
        "category": Listing.objects.filter(category=listing.category),
        "latest_bid": Listing.objects.filter(latest_bid=listing.latest_bid),
        'price': price,
        'bid_form': BidForm(),
        'comments': listing.listing_comment.all().order_by('-date_posted'),        
        'comment_form': CommentForm()
        })
  

""" ===============BID VIEW PART================ """
@login_required(login_url="login")
def listing_bid(request, listing_slug):
    
    listing = Listing.objects.get(slug=listing_slug)
    bid = int(request.POST.get('bid', False))  #False to catch empty value for bid
   
    if  bid > listing.price and (listing.latest_bid is None or bid > listing.latest_bid):
        
        listing.latest_bid = bid
        form = BidForm(request.POST)
        new_bid = form.save(commit=False)
        new_bid.listing = listing
        new_bid.raiser = request.user
        listing.winner = new_bid.raiser
        new_bid.save()
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=[listing_slug]))
                
    else:
        if request.user in listing.watching.all():
            listing.is_watched = True
        else:
            listing.is_watched = False

        return render(request, "auctions/listing.html", {
            'listing': listing,
            'title': listing.title,
            'image': listing.image,
            'category': Listing.objects.filter(category=listing.category),
            'latest_bid': listing.latest_bid,
            'bid_form': BidForm(),
            'comments': listing.listing_comment.all(),
            'comment_form': CommentForm(),
            'message': "Your bid must be higher than "
            })


""" ===============COMMENT VIEW PART================ """
@login_required(login_url="login")
def listing_comment(request, listing_slug):

    listing = Listing.objects.get(slug=listing_slug)
    form = CommentForm(request.POST)
    new_comment = form.save(commit=False)
    new_comment.user = request.user
    new_comment.listing = listing
    new_comment.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_slug]))


""" ============LISTING_CLOSE VIEW PART============= """
@login_required
def listing_close(request, listing_slug):

    listing = Listing.objects.get(slug=listing_slug)
    
    while request.user == listing.owner:
        
        if listing.winner:
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_slug]))
        else:
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse("index"))


""" ============ CATEGORIES VIEW PART ============= """
def categories(request):
    categories = Listing.objects.order_by().values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html",{
        "categories" : categories
    })


def category(request, category):
    listings = Listing.objects.filter(category = category).all()
    return render(request, "auctions/category.html",{
        "listings" : listings,
        "category": category
    })