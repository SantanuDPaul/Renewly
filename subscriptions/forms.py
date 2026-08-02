from django import forms
from django.core.exceptions import ValidationError
from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['service_name',
                  'category',
                  'price', 
                  'billing_cycle', 
                  'currency',
                  'start_date', 
                  'renewal_date',
                  'payment_method',
                  'website',
                  'notes'
            ]
        widgets = {
            "service_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Netflix",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 499",
                }
            ),

            "billing_cycle": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "currency": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "renewal_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Optional notes...",
                }
            ),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select a category"
        self.fields["billing_cycle"].label = "Billing Cycle"
        self.fields["payment_method"].label = "Payment Method"
        self.fields["renewal_date"].label = "Renewal Date"
        self.fields["start_date"].label = "Start Date"

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        renewal_date = cleaned_data.get("renewal_date")
        price = cleaned_data.get("price")

        if start_date and renewal_date:
            if renewal_date < start_date:
                self.add_error(
                    "renewal_date",
                    "Renewal date cannot be earlier than the start date."
                )

        if price is not None:
            if price <= 0:
                self.add_error(
                    "price",
                    "Price must be greater than zero."
                )

        return cleaned_data
       