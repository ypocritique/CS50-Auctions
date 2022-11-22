from tkinter import Widget
from django import forms
from django.forms import ModelForm, URLInput
from .models import Listing, Bid, Comment



class ListingForm(ModelForm):
	
	class Meta:
		model = Listing
		fields = ['title', 'category','description', 'price', 'image']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title'}),
			'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'category'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
			'image': forms.URLInput(attrs={"class": "user_input"})
            
            }


class BidForm(ModelForm):
	bid = forms.CharField(label='', required=False, widget=forms.NumberInput(attrs={
		'class': 'form-control', 'placeholder': 'place your bid here'
		}))
	class Meta:
		model = Bid
		fields = ['bid']


class CommentForm(ModelForm):
	comment = forms.CharField(label='', widget=forms.TextInput(attrs={
		'class': 'form-control', 'placeholder': 'Add a comment here'
		}))
	class Meta:
		model = Comment
		fields = ['comment']

