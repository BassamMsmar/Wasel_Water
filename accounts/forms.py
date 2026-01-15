from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'full_name', 'phone_number', 'city', 'neighborhood', 
            'street', 'building_number', 'apartment_number', 
            'image_of_building', 'address_type', 'is_default'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الكامل'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الحي'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الشارع'}),
            'building_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم المبنى'}),
            'apartment_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الشقة (اختياري)'}),
            'address_type': forms.Select(attrs={'class': 'form-select'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
