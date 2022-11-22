from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("listing/<slug:listing_slug>/", views.listing, name="listing"),
    path("listing/watchlist/<slug:listing_slug>", views.watch_edition, name="watch_edition"),
    path("listing/<slug:listing_slug>/bid/", views.listing_bid, name="listing_bid"),
    path("listing/<slug:listing_slug>/comments", views.listing_comment, name="listing_comment"),
    path("listing/<slug:listing_slug>/close", views.listing_close, name="listing_close"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category")
    
]