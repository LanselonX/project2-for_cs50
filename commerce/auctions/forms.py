from django import forms

from .models import AuctionList, Lot, Commentary

class AddListingForm(forms.ModelForm):
    class Meta:
        model = AuctionList
        fields = ['title', 'description', 'start_price', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description'
            }),
        }

class AddLotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = ['lot_bid']
        labels = {
            'lot_bid': 'Choose your bid',
        }
        widgets = {
            'lot_bid': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your bid'
            })
        }

class AddCommentaryForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ['text']
        labels ={
            'text': 'Commentary',
        }
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter commentary'
            })
        }

class CloseAuctionForm(forms.ModelForm):
    class Meta:
        model = AuctionList
        fields = ['is_active']