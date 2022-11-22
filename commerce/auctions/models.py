
from multiprocessing import Value
from optparse import Values
from typing import ValuesView
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    pass


class Listing(models.Model):
    category = models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing_owner')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.URLField(default='https://picsum.photos/id/532/800/500')
    #image = models.ImageField(upload_to='images/',null=True, blank=True,)
    slug = models.SlugField(max_length=255)
    price = models.PositiveIntegerField(null=True, blank=True)
    latest_bid = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    watching = models.ManyToManyField(User, related_name='watchlist', blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'listings'
        

    def get_absolute_url(self):
        return reverse('auctions:listing', args=[self.slug])

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_bid')
    raiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="raiser", null=True, blank=True)
    bid = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
        

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_comment')
    comment = models.TextField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)


    
