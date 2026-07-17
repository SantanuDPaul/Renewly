from django import forms
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
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'renewal_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select a category"
       